#!/usr/bin/env python3
"""
Gmail Watcher - Monitors Gmail inbox for important emails
Part of Silver Tier implementation
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import json
import logging
import pickle

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))
from base_watcher import BaseWatcher

# Try to import Gmail API, fall back to mock if not available
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    GMAIL_API_AVAILABLE = True
except ImportError:
    GMAIL_API_AVAILABLE = False
    print("Warning: Gmail API libraries not installed. Using mock mode.")
    print("Install with: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")


class GmailService:
    """Real Gmail API service"""

    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    def __init__(self, credentials_path: str):
        self.credentials_path = credentials_path
        self.token_path = Path(credentials_path).parent / 'token.pickle'
        self.service = self._authenticate()

    def _authenticate(self):
        """Authenticate with Gmail API"""
        creds = None

        # Load existing token
        if self.token_path.exists():
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)

        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES)
                creds = flow.run_local_server(port=0)

            # Save credentials
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)

        return build('gmail', 'v1', credentials=creds)

    def list_messages(self, query: str = 'is:unread is:important'):
        """List messages matching query"""
        try:
            results = self.service.users().messages().list(
                userId='me', q=query, maxResults=10).execute()
            return results.get('messages', [])
        except Exception as e:
            print(f"Error listing messages: {e}")
            return []

    def get_message(self, message_id: str):
        """Get full message details"""
        try:
            return self.service.users().messages().get(
                userId='me', id=message_id, format='full').execute()
        except Exception as e:
            print(f"Error getting message: {e}")
            return None


class MockGmailService:
    """Mock Gmail service for demonstration when API not available"""

    def __init__(self, credentials_path: str):
        self.credentials_path = credentials_path

    def list_messages(self, query: str = 'is:unread is:important'):
        """Mock method - returns empty list"""
        return []

    def get_message(self, message_id: str):
        """Mock method - returns sample message"""
        return {
            'id': message_id,
            'snippet': 'This is a sample email content...',
            'payload': {
                'headers': [
                    {'name': 'From', 'value': 'client@example.com'},
                    {'name': 'Subject', 'value': 'Important: Project Update'},
                    {'name': 'Date', 'value': datetime.now().isoformat()}
                ]
            }
        }


class GmailWatcher(BaseWatcher):
    """Watches Gmail inbox for important emails and creates action items"""

    def __init__(self, vault_path: str, credentials_path: str = None):
        super().__init__(vault_path, check_interval=120)  # Check every 2 minutes

        # Use credentials.json from project root if not provided
        if credentials_path is None:
            project_root = Path(__file__).parent.parent
            credentials_path = str(project_root / 'credentials.json')

        self.credentials_path = credentials_path

        # Use real Gmail API if available and credentials exist, otherwise mock
        if GMAIL_API_AVAILABLE and Path(credentials_path).exists():
            try:
                self.service = GmailService(credentials_path)
                self.logger.info("Using real Gmail API")
            except Exception as e:
                self.logger.warning(f"Failed to initialize Gmail API: {e}. Using mock mode.")
                self.service = MockGmailService(credentials_path)
        else:
            self.logger.info("Using mock Gmail service (API not available or credentials missing)")
            self.service = MockGmailService(credentials_path)

        self.processed_ids = set()

        # Load processed IDs from state file
        self.state_file = Path(__file__).parent / '.gmail_watcher_state.json'
        self._load_state()

    def _load_state(self):
        """Load previously processed message IDs"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                    self.processed_ids = set(state.get('processed_ids', []))
            except Exception as e:
                self.logger.warning(f'Could not load state: {e}')

    def _save_state(self):
        """Save processed message IDs"""
        try:
            with open(self.state_file, 'w') as f:
                json.dump({'processed_ids': list(self.processed_ids)}, f)
        except Exception as e:
            self.logger.error(f'Could not save state: {e}')

    def check_for_updates(self) -> list:
        """Check Gmail for new important/unread messages"""
        try:
            messages = self.service.list_messages('is:unread is:important')
            new_messages = [m for m in messages if m.get('id') not in self.processed_ids]

            if new_messages:
                self.logger.info(f'Found {len(new_messages)} new important emails')

            return new_messages
        except Exception as e:
            self.logger.error(f'Error checking Gmail: {e}')
            return []

    def create_action_file(self, message) -> Path:
        """Create action file for email in Needs_Action folder"""
        try:
            message_id = message.get('id', 'unknown')
            msg_details = self.service.get_message(message_id)

            # Extract headers
            headers = {h['name']: h['value']
                      for h in msg_details.get('payload', {}).get('headers', [])}

            # Create action file content
            content = f"""---
type: email
source: gmail
from: {headers.get('From', 'Unknown')}
subject: {headers.get('Subject', 'No Subject')}
received: {datetime.now().isoformat()}
priority: high
status: pending
message_id: {message_id}
---

## Email Content

{msg_details.get('snippet', 'No content available')}

## Suggested Actions

- [ ] Read and understand the email
- [ ] Draft a reply if needed
- [ ] Forward to relevant party if needed
- [ ] Archive after processing

## Notes

This email was flagged as important. Review and take appropriate action.
"""

            # Create unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_subject = ''.join(c for c in headers.get('Subject', 'email')[:30]
                                  if c.isalnum() or c in (' ', '-', '_')).strip().replace(' ', '_')
            filename = f'EMAIL_{timestamp}_{safe_subject}.md'
            filepath = self.needs_action / filename

            # Write file
            filepath.write_text(content, encoding='utf-8')

            # Mark as processed
            self.processed_ids.add(message_id)
            self._save_state()

            self.logger.info(f'Created action file: {filename}')
            return filepath

        except Exception as e:
            self.logger.error(f'Error creating action file: {e}')
            raise


def main():
    """Main entry point for Gmail watcher"""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Get vault path
    vault_path = Path(__file__).parent.parent / 'AI_Employee_Vault'

    # Create and run watcher
    watcher = GmailWatcher(str(vault_path))

    print(f"Gmail Watcher started")
    print(f"Vault: {vault_path}")
    print(f"Check interval: {watcher.check_interval} seconds")
    print(f"Monitoring for important/unread emails...")
    print("Press Ctrl+C to stop\n")

    try:
        watcher.run()
    except KeyboardInterrupt:
        print("\nGmail Watcher stopped by user")
        sys.exit(0)


if __name__ == '__main__':
    main()
