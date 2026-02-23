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

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))
from base_watcher import BaseWatcher

# Mock Gmail API for demonstration (replace with real API in production)
class MockGmailService:
    """Mock Gmail service for demonstration purposes"""

    def __init__(self, credentials_path: str):
        self.credentials_path = credentials_path
        self.processed_ids = set()

    def list_messages(self, query: str = 'is:unread is:important'):
        """Mock method - returns sample unread messages"""
        # In production, this would use Google API:
        # from google.oauth2.credentials import Credentials
        # from googleapiclient.discovery import build
        # service = build('gmail', 'v1', credentials=creds)
        # results = service.users().messages().list(userId='me', q=query).execute()

        # For demo, return empty list (no mock emails)
        return []

    def get_message(self, message_id: str):
        """Mock method - returns message details"""
        # In production: service.users().messages().get(userId='me', id=message_id).execute()
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

        # Use mock credentials path if not provided
        if credentials_path is None:
            credentials_path = str(Path(__file__).parent / 'mock_gmail_credentials.json')

        self.credentials_path = credentials_path
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
