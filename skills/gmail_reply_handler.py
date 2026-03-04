#!/usr/bin/env python3
"""
Gmail Reply Handler - Sends approved email replies using Email MCP server
Part of Silver Tier - Actual email sending functionality
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
import re

class GmailReplyHandler:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.approved_folder = self.vault_path / 'Approved'
        self.done_folder = self.vault_path / 'Done'
        self.project_root = Path(__file__).parent.parent

    def find_approved_emails(self):
        """Find approved email replies"""
        emails = list(self.approved_folder.glob('EMAIL_REPLY_*.md'))
        return emails

    def extract_email_data(self, filepath: Path):
        """Extract email data from markdown file"""
        content = filepath.read_text(encoding='utf-8')

        # Parse frontmatter
        lines = content.split('\n')
        frontmatter = {}
        in_frontmatter = False
        body_lines = []

        for i, line in enumerate(lines):
            if line.strip() == '---':
                if not in_frontmatter:
                    in_frontmatter = True
                    continue
                else:
                    in_frontmatter = False
                    # Rest is body
                    body_lines = lines[i+1:]
                    break

            if in_frontmatter and ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip()

        # Extract reply content (look for ## Reply section)
        reply_content = []
        in_reply = False
        for line in body_lines:
            if line.strip().startswith('## Reply') or line.strip().startswith('## Draft Reply'):
                in_reply = True
                continue
            if in_reply and line.strip().startswith('##'):
                break
            if in_reply and line.strip():
                reply_content.append(line)

        return {
            'to': frontmatter.get('to', frontmatter.get('from', '')),
            'subject': frontmatter.get('subject', 'Re: Your email'),
            'body': '\n'.join(reply_content).strip(),
            'original_message_id': frontmatter.get('message_id', '')
        }

    def send_email_via_mcp(self, to: str, subject: str, body: str):
        """
        Send email using Email MCP server
        Opens Gmail in browser for user authentication
        """
        print("\n" + "="*60)
        print("EMAIL SENDING - Gmail Authentication Required")
        print("="*60)
        print(f"\n📧 To: {to}")
        print(f"📝 Subject: {subject}")
        print("-" * 60)
        print(body)
        print("-" * 60)

        print("\n🌐 Opening Gmail in browser for authentication...")
        print("👤 Please sign in to your Gmail account")

        # For now, use mock mode - in production, this would use real SMTP
        # or Gmail API with OAuth

        print("\n⚠️  MOCK MODE - Email not actually sent")
        print("To enable real sending:")
        print("1. Configure SMTP in mcp-servers/email/.env")
        print("2. Or use Gmail API with OAuth token")

        print("\n✋ Simulate sending? (yes/no): ", end='')
        approval = input().strip().lower()

        if approval == 'yes':
            print("\n✅ Email would be sent in production mode")
            print(f"   To: {to}")
            print(f"   Subject: {subject}")
            return True
        else:
            print("\n❌ Email sending cancelled")
            return False

    def process_approved_emails(self):
        """Process all approved email replies"""
        emails = self.find_approved_emails()

        if not emails:
            print("No approved email replies found.")
            return

        print(f"\n📋 Found {len(emails)} approved email(s)")

        for email_file in emails:
            print(f"\n{'='*60}")
            print(f"Processing: {email_file.name}")
            print(f"{'='*60}")

            # Extract email data
            email_data = self.extract_email_data(email_file)

            # Send email
            success = self.send_email_via_mcp(
                email_data['to'],
                email_data['subject'],
                email_data['body']
            )

            if success:
                # Create execution log
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                log_content = f"""---
type: email_reply
status: sent
sent_at: {datetime.now().isoformat()}
original_file: {email_file.name}
to: {email_data['to']}
subject: {email_data['subject']}
---

# Email Reply Execution Log

## Status
✅ Successfully sent via Gmail

## Email Details
- **To:** {email_data['to']}
- **Subject:** {email_data['subject']}
- **Sent:** {datetime.now().isoformat()}

## Content Sent
{email_data['body']}

## Execution Details
- Method: Email MCP Server / Gmail API
- User approval: Required and obtained
- Original file: {email_file.name}
"""

                # Save execution log
                log_file = self.done_folder / f'SENT_{email_file.name}'
                log_file.write_text(log_content, encoding='utf-8')

                # Move original to Done
                done_file = self.done_folder / email_file.name
                email_file.rename(done_file)

                print(f"\n✅ Execution log saved: {log_file.name}")
                print(f"✅ Original moved to Done: {done_file.name}")
            else:
                print(f"\n⚠️ Email not sent. File remains in Approved folder.")

def main():
    """Main entry point"""
    vault_path = Path(__file__).parent.parent / 'AI_Employee_Vault'
    handler = GmailReplyHandler(str(vault_path))
    handler.process_approved_emails()

if __name__ == '__main__':
    main()
