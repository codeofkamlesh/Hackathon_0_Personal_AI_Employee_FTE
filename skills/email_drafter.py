#!/usr/bin/env python3
"""
Email Drafter - Creates email reply drafts with HITL approval workflow
Analyzes incoming emails and drafts appropriate responses
"""

import sys
from pathlib import Path
from datetime import datetime
import json

class EmailDrafter:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.company_handbook = self.vault_path / 'Company_Handbook.md'

    def find_email_actions(self):
        """Find email action items that need replies"""
        emails = list(self.needs_action.glob('EMAIL_*.md'))
        return emails

    def extract_email_info(self, filepath: Path):
        """Extract email information from action file"""
        content = filepath.read_text(encoding='utf-8')

        lines = content.split('\n')
        frontmatter = {}
        in_frontmatter = False

        for line in lines:
            if line.strip() == '---':
                if not in_frontmatter:
                    in_frontmatter = True
                    continue
                else:
                    break

            if in_frontmatter and ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip()

        return frontmatter

    def draft_reply(self, email_info: dict):
        """Draft a reply based on email information"""
        sender = email_info.get('from', 'Unknown')
        subject = email_info.get('subject', 'No Subject')

        # Simple reply template - in production, Claude would draft this
        reply = f"""Thank you for your email regarding "{subject}".

I have received your message and will review it carefully. I will get back to you with a detailed response shortly.

If this is urgent, please feel free to reach out directly.

Best regards"""

        return reply

    def create_reply_draft(self, email_file: Path):
        """Create a reply draft for approval"""
        email_info = self.extract_email_info(email_file)
        reply_content = self.draft_reply(email_info)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        sender = email_info.get('from', 'unknown').split('@')[0]

        draft_content = f"""---
type: email_reply
source: email_drafter
to: {email_info.get('from', '')}
subject: Re: {email_info.get('subject', '')}
created: {datetime.now().isoformat()}
priority: medium
status: pending_approval
requires_approval: true
message_id: {email_info.get('message_id', '')}
---

# Email Reply Draft

## Original Email
- **From:** {email_info.get('from', 'Unknown')}
- **Subject:** {email_info.get('subject', 'No Subject')}
- **Received:** {email_info.get('received', 'Unknown')}

## Draft Reply

{reply_content}

## Approval Instructions

1. **Review** the draft reply above
2. **Edit** if needed (modify the content directly)
3. **Approve:** Move this file to `/Approved` folder
4. **Reject:** Move this file to `/Rejected` folder

## Notes

- Reply will be sent from your Gmail account
- You can edit the reply content before approving
- Original email file: {email_file.name}
"""

        # Save draft to Pending_Approval
        draft_file = self.pending_approval / f'EMAIL_REPLY_{timestamp}_{sender}.md'
        draft_file.write_text(draft_content, encoding='utf-8')

        # Move original email to Done (processed)
        done_folder = self.vault_path / 'Done'
        done_file = done_folder / email_file.name
        email_file.rename(done_file)

        return draft_file

    def process_emails(self):
        """Process all email action items"""
        emails = self.find_email_actions()

        if not emails:
            print("No email action items found.")
            return

        print(f"\n📧 Found {len(emails)} email(s) to process")

        for email_file in emails:
            print(f"\n{'='*60}")
            print(f"Processing: {email_file.name}")
            print(f"{'='*60}")

            draft_file = self.create_reply_draft(email_file)
            print(f"✅ Reply draft created: {draft_file.name}")
            print(f"📁 Location: {draft_file}")
            print(f"👉 Review and move to /Approved to send")

def main():
    """Main entry point"""
    vault_path = Path(__file__).parent.parent / 'AI_Employee_Vault'
    drafter = EmailDrafter(str(vault_path))
    drafter.process_emails()

if __name__ == '__main__':
    main()
