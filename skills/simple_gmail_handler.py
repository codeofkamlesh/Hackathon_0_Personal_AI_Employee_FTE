#!/usr/bin/env python3
"""
Simple Gmail Reply Handler - Opens Gmail in browser for sending
Uses Playwright directly for real browser interaction
"""

import sys
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright

class SimpleGmailReplyHandler:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.approved_folder = self.vault_path / 'Approved'
        self.done_folder = self.vault_path / 'Done'

    def find_approved_emails(self):
        """Find approved email replies"""
        return list(self.approved_folder.glob('EMAIL_REPLY_*.md'))

    def extract_email_data(self, filepath: Path):
        """Extract email data from markdown file"""
        content = filepath.read_text(encoding='utf-8')
        lines = content.split('\n')

        # Parse frontmatter
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
                    body_lines = lines[i+1:]
                    break

            if in_frontmatter and ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip()

        # Extract reply content
        reply_content = []
        in_reply = False
        for line in body_lines:
            if '## Draft Reply' in line or '## Reply' in line:
                in_reply = True
                continue
            if in_reply and line.strip().startswith('##'):
                break
            if in_reply and line.strip():
                reply_content.append(line)

        return {
            'to': frontmatter.get('to', ''),
            'subject': frontmatter.get('subject', 'Re: Your email'),
            'body': '\n'.join(reply_content).strip()
        }

    def send_email_via_browser(self, to: str, subject: str, body: str):
        """
        Send email via Gmail in browser
        Opens REAL browser window for user interaction
        """
        print("\n" + "="*70)
        print("GMAIL REPLY - Real Browser Window")
        print("="*70)
        print(f"\n📧 To: {to}")
        print(f"📝 Subject: {subject}")
        print("-" * 70)
        print(body)
        print("-" * 70)

        print("\n🌐 Opening Gmail in browser...")
        print("👤 You will sign in and send manually")
        print("")

        try:
            with sync_playwright() as p:
                # Launch browser in NON-HEADLESS mode
                print("🚀 Launching browser...")
                browser = p.chromium.launch(headless=False, slow_mo=1000)
                context = browser.new_context()
                page = context.new_page()

                # Navigate to Gmail
                print("📧 Opening Gmail...")
                page.goto('https://mail.google.com')

                print("\n" + "="*70)
                print("MANUAL STEPS - Follow these in the browser:")
                print("="*70)
                print("1. Sign in to your Gmail account")
                print("2. Click 'Compose' button")
                print(f"3. To: {to}")
                print(f"4. Subject: {subject}")
                print("5. Copy the email body shown above")
                print("6. Paste it into the email")
                print("7. Click 'Send' button")
                print("="*70)
                print("\nPress ENTER here after you've sent the email...")

                input()

                print("\n✅ Email sent!")

                browser.close()
                return True

        except Exception as e:
            print(f"\n❌ Error: {e}")
            return False

    def process_approved_emails(self):
        """Process all approved email replies"""
        emails = self.find_approved_emails()

        if not emails:
            print("No approved email replies found.")
            return

        print(f"\n📋 Found {len(emails)} approved email(s)\n")

        for email_file in emails:
            print(f"{'='*70}")
            print(f"Processing: {email_file.name}")
            print(f"{'='*70}\n")

            # Extract email data
            email_data = self.extract_email_data(email_file)

            # Send email
            success = self.send_email_via_browser(
                email_data['to'],
                email_data['subject'],
                email_data['body']
            )

            if success:
                # Create execution log
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
- Method: Manual sending via browser
- User confirmation: Obtained
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
    handler = SimpleGmailReplyHandler(str(vault_path))
    handler.process_approved_emails()

if __name__ == '__main__':
    main()
