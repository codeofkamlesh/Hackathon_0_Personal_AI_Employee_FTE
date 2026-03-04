#!/usr/bin/env python3
"""
Automated Gmail Reply Handler - Browser automation with Playwright
Opens Chromium, user signs in once, then auto-composes and sends email
Part of Silver Tier - Same experience as LinkedIn automation
"""

import sys
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time

class AutomatedGmailHandler:
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

    def send_email_automated(self, to: str, subject: str, body: str):
        """
        Automated Gmail sending with Playwright
        Opens Chromium, user signs in once (saved), then auto-composes and sends
        """
        print("\n" + "="*70)
        print("📧 AUTOMATED GMAIL SENDING")
        print("="*70)
        print(f"\n📬 To: {to}")
        print(f"📝 Subject: {subject}")
        print("-" * 70)
        print(body)
        print("-" * 70)

        try:
            with sync_playwright() as p:
                print("\n🚀 Launching Chromium browser...")

                # Use persistent context to save login session
                user_data_dir = Path(__file__).parent.parent / '.browser_data' / 'gmail'
                user_data_dir.mkdir(parents=True, exist_ok=True)

                print(f"📁 Using persistent browser profile: {user_data_dir}")
                print("   (Your sign-in will be saved for next time)")

                # Launch persistent context (saves cookies, login, etc.)
                context = p.chromium.launch_persistent_context(
                    str(user_data_dir),
                    headless=False,
                    slow_mo=1000,  # Slow down for visibility
                    args=['--start-maximized']
                )

                page = context.pages[0] if context.pages else context.new_page()

                # Navigate to Gmail
                print("📧 Opening Gmail...")
                page.goto('https://mail.google.com/mail/u/0/#inbox', timeout=60000)

                # Wait for user to sign in if needed
                print("\n" + "="*70)
                print("👤 SIGN IN TO GMAIL")
                print("="*70)
                print("If you see a sign-in page, please sign in now.")
                print("Press ENTER after you see your Gmail inbox...")
                print("="*70)
                input()

                print("\n✅ Signed in! Starting automation...")
                time.sleep(3)

                # Click Compose button
                print("🤖 Clicking 'Compose' button...")
                try:
                    # Try multiple selectors for Compose button
                    compose_clicked = False

                    # Method 1: Text-based
                    try:
                        page.click('div[role="button"]:has-text("Compose")', timeout=5000)
                        compose_clicked = True
                    except:
                        pass

                    # Method 2: Class-based (Gmail's compose button class)
                    if not compose_clicked:
                        try:
                            page.click('.T-I.T-I-KE.L3', timeout=5000)
                            compose_clicked = True
                        except:
                            pass

                    # Method 3: Aria label
                    if not compose_clicked:
                        try:
                            page.click('[aria-label*="Compose"]', timeout=5000)
                            compose_clicked = True
                        except:
                            pass

                    if not compose_clicked:
                        print("⚠️  Could not find Compose button automatically")
                        print("Please click 'Compose' manually, then press ENTER...")
                        input()

                except Exception as e:
                    print(f"⚠️  Compose button error: {e}")
                    print("Please click 'Compose' manually, then press ENTER...")
                    input()

                time.sleep(3)

                # Fill To field
                print(f"🤖 Filling 'To' field: {to}")
                try:
                    # Wait for compose window to appear
                    page.wait_for_selector('input[name="to"], textarea[name="to"], input[aria-label*="To"]', timeout=10000)

                    # Try different selectors for To field
                    to_filled = False

                    # Method 1: name attribute
                    try:
                        page.fill('input[name="to"]', to, timeout=3000)
                        to_filled = True
                    except:
                        pass

                    # Method 2: textarea
                    if not to_filled:
                        try:
                            page.fill('textarea[name="to"]', to, timeout=3000)
                            to_filled = True
                        except:
                            pass

                    # Method 3: aria-label
                    if not to_filled:
                        try:
                            page.fill('input[aria-label*="To"]', to, timeout=3000)
                            to_filled = True
                        except:
                            pass

                    if not to_filled:
                        print(f"⚠️  Could not auto-fill To field")
                        print(f"Please type: {to}")
                        print("Then press ENTER...")
                        input()

                    time.sleep(1)
                    page.keyboard.press('Tab')

                except Exception as e:
                    print(f"⚠️  To field error: {e}")
                    print(f"Please type: {to}")
                    print("Then press ENTER...")
                    input()

                # Fill Subject field
                print(f"🤖 Filling 'Subject' field: {subject}")
                try:
                    subject_filled = False

                    # Method 1: name attribute
                    try:
                        page.fill('input[name="subjectbox"]', subject, timeout=3000)
                        subject_filled = True
                    except:
                        pass

                    # Method 2: aria-label
                    if not subject_filled:
                        try:
                            page.fill('input[aria-label*="Subject"]', subject, timeout=3000)
                            subject_filled = True
                        except:
                            pass

                    # Method 3: Just type it (we're already in subject field after Tab)
                    if not subject_filled:
                        page.keyboard.type(subject)
                        subject_filled = True

                    time.sleep(1)
                    page.keyboard.press('Tab')

                except Exception as e:
                    print(f"⚠️  Subject field error: {e}")
                    print(f"Please type: {subject}")
                    print("Then press ENTER...")
                    input()

                # Fill Body
                print("🤖 Filling email body...")
                try:
                    body_filled = False

                    # Method 1: role=textbox
                    try:
                        page.fill('div[role="textbox"][aria-label*="Message"]', body, timeout=3000)
                        body_filled = True
                    except:
                        pass

                    # Method 2: contenteditable
                    if not body_filled:
                        try:
                            page.fill('div[contenteditable="true"][aria-label*="Message"]', body, timeout=3000)
                            body_filled = True
                        except:
                            pass

                    # Method 3: Just type it (we're in body after Tab)
                    if not body_filled:
                        page.keyboard.type(body)
                        body_filled = True

                    time.sleep(2)

                except Exception as e:
                    print(f"⚠️  Body field error: {e}")
                    print("Please type the email body manually")
                    print("Then press ENTER...")
                    input()

                # Final review before sending
                print("\n" + "="*70)
                print("✅ EMAIL COMPOSED - READY TO SEND")
                print("="*70)
                print("Review the email in the browser window.")
                print("Type 'SEND' to send, or 'CANCEL' to abort: ", end='')
                approval = input().strip().upper()
                print("="*70)

                if approval == 'SEND':
                    # Click Send button
                    print("\n🤖 Clicking 'Send' button...")
                    try:
                        send_clicked = False

                        # Method 1: Text-based
                        try:
                            page.click('div[role="button"]:has-text("Send")', timeout=5000)
                            send_clicked = True
                        except:
                            pass

                        # Method 2: Gmail's send button class
                        if not send_clicked:
                            try:
                                page.click('.T-I.J-J5-Ji.aoO.v7.T-I-atl.L3', timeout=5000)
                                send_clicked = True
                            except:
                                pass

                        # Method 3: Aria label
                        if not send_clicked:
                            try:
                                page.click('[aria-label*="Send"]', timeout=5000)
                                send_clicked = True
                            except:
                                pass

                        # Method 4: Keyboard shortcut
                        if not send_clicked:
                            print("Using keyboard shortcut Ctrl+Enter...")
                            page.keyboard.press('Control+Enter')
                            send_clicked = True

                        time.sleep(3)
                        print("\n✅ Email sent successfully!")

                        # Keep browser open for verification
                        print("\n" + "="*70)
                        print("✅ EMAIL SENT - Browser will stay open")
                        print("="*70)
                        print("You can verify the email was sent in Gmail.")
                        print("Press ENTER to close browser and continue...")
                        print("="*70)
                        input()

                        context.close()
                        return True

                    except Exception as e:
                        print(f"⚠️  Send button error: {e}")
                        print("Please click 'Send' manually, then press ENTER...")
                        input()
                        context.close()
                        return True
                else:
                    print("\n❌ Email cancelled by user")
                    context.close()
                    return False

        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("\nTroubleshooting:")
            print("1. Make sure Chromium is installed: playwright install chromium")
            print("2. Check your internet connection")
            print("3. Try running: ./install_browser_deps.sh")
            return False

    def process_approved_emails(self):
        """Process ONE approved email reply (prevents infinite loops)"""
        emails = self.find_approved_emails()

        if not emails:
            print("\n📭 No approved email replies found in Approved folder.")
            print(f"   Looking in: {self.approved_folder}")
            return

        print(f"\n📋 Found {len(emails)} approved email(s) to send")
        print("   Processing FIRST email only (to prevent loops)\n")

        # Process only the FIRST email
        email_file = emails[0]

        print(f"{'='*70}")
        print(f"Processing: {email_file.name}")
        print(f"{'='*70}\n")

        email_data = self.extract_email_data(email_file)

        if not email_data['to']:
            print(f"⚠️  ERROR: No recipient email found")
            return

        if not email_data['body']:
            print(f"⚠️  ERROR: No email body found")
            return

        success = self.send_email_automated(
            email_data['to'],
            email_data['subject'],
            email_data['body']
        )

        if success:
            log_content = f"""---
type: email_reply
status: sent
sent_at: {datetime.now().isoformat()}
original_file: {email_file.name}
to: {email_data['to']}
subject: {email_data['subject']}
method: browser_automation
---

# Email Reply Execution Log

## Status
✅ Successfully sent via Gmail (Browser Automation)

## Email Details
- **To:** {email_data['to']}
- **Subject:** {email_data['subject']}
- **Sent:** {datetime.now().isoformat()}
- **Method:** Playwright Browser Automation

## Content Sent
{email_data['body']}

## Execution Details
- Browser: Chromium (Playwright)
- User sign-in: Saved in persistent profile
- Auto-compose: Yes
- Auto-send: Yes (with HITL approval)
- Original file: {email_file.name}

---
*Sent by AI Employee - Silver Tier Gmail Automation*
"""

            log_file = self.done_folder / f'SENT_{email_file.name}'
            log_file.write_text(log_content, encoding='utf-8')

            done_file = self.done_folder / email_file.name
            email_file.rename(done_file)

            print(f"\n✅ Execution log saved: {log_file.name}")
            print(f"✅ Original moved to Done: {done_file.name}")
            print(f"\n{'='*70}\n")
        else:
            print(f"\n⚠️  Email not sent. File remains in Approved folder.")
            print(f"{'='*70}\n")


def main():
    """Main entry point"""
    print("\n" + "="*70)
    print("AUTOMATED GMAIL HANDLER - Silver Tier")
    print("Browser automation with Chromium (like LinkedIn)")
    print("="*70)

    vault_path = Path(__file__).parent.parent / 'AI_Employee_Vault'

    if not vault_path.exists():
        print(f"\n❌ ERROR: Vault not found at {vault_path}")
        sys.exit(1)

    try:
        handler = AutomatedGmailHandler(str(vault_path))
        handler.process_approved_emails()

        print("\n" + "="*70)
        print("✅ AUTOMATED GMAIL HANDLER COMPLETE")
        print("="*70)

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
