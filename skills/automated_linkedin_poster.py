#!/usr/bin/env python3
"""
Automated LinkedIn Poster - Full automation with HITL approval
Only manual steps: Sign-in and final approval
"""

import sys
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright
import time

class AutomatedLinkedInPoster:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.approved_folder = self.vault_path / 'Approved'
        self.done_folder = self.vault_path / 'Done'

    def find_approved_posts(self):
        """Find approved LinkedIn posts"""
        return list(self.approved_folder.glob('LINKEDIN_POST_*.md'))

    def extract_post_content(self, filepath: Path):
        """Extract clean post content"""
        content = filepath.read_text(encoding='utf-8')
        lines = content.split('\n')

        # Skip frontmatter and extract main content
        in_frontmatter = False
        post_lines = []

        for line in lines:
            if line.strip() == '---':
                in_frontmatter = not in_frontmatter
                continue
            if not in_frontmatter and line.strip():
                # Skip headers, checklists, and instructions
                if not line.startswith('#') and not line.strip().startswith('- ['):
                    if 'automatically drafted' not in line.lower() and 'silver tier' not in line.lower():
                        post_lines.append(line)

        return '\n'.join(post_lines).strip()

    def post_to_linkedin_automated(self, content: str):
        """
        Automated LinkedIn posting with Playwright
        Uses persistent context to save sign-in
        """
        print("\n" + "="*70)
        print("AUTOMATED LINKEDIN POSTING")
        print("="*70)
        print(f"\n📝 Content to post:")
        print("-" * 70)
        print(content)
        print("-" * 70)

        try:
            with sync_playwright() as p:
                print("\n🚀 Launching browser...")

                # Use persistent context to save login session
                user_data_dir = Path(__file__).parent.parent / '.browser_data' / 'linkedin'
                user_data_dir.mkdir(parents=True, exist_ok=True)

                print(f"📁 Using persistent browser profile: {user_data_dir}")
                print("   (Your sign-in will be saved for next time)")

                # Launch persistent context (saves cookies, login, etc.)
                context = p.chromium.launch_persistent_context(
                    str(user_data_dir),
                    headless=False,
                    slow_mo=500,
                    args=['--start-maximized']
                )

                page = context.pages[0] if context.pages else context.new_page()

                # Navigate to LinkedIn
                print("📱 Opening LinkedIn...")
                page.goto('https://www.linkedin.com/feed/')

                print("\n" + "="*70)
                print("⏸️  MANUAL STEP 1: SIGN IN")
                print("="*70)
                print("Please sign in to LinkedIn in the browser window")
                print("Press ENTER here after you're signed in and see your feed...")
                print("="*70)
                input()

                print("\n✅ Signed in! Starting automation...")
                time.sleep(2)

                # Automated: Click "Start a post"
                print("🤖 Clicking 'Start a post' button...")
                try:
                    # Try multiple selectors
                    page.click('button:has-text("Start a post")', timeout=5000)
                except:
                    try:
                        page.click('[aria-label*="Start a post"]', timeout=5000)
                    except:
                        # Force click using JavaScript
                        page.evaluate('document.querySelector(\'[aria-label*="Start a post"]\').click()')

                time.sleep(3)

                # Automated: Fill in the post content
                print("🤖 Filling in post content...")
                try:
                    page.fill('div[role="textbox"]', content)
                except:
                    try:
                        page.fill('div[contenteditable="true"]', content)
                    except:
                        # Use keyboard to type
                        page.keyboard.type(content)

                time.sleep(2)

                print("\n" + "="*70)
                print("⏸️  MANUAL STEP 2: FINAL APPROVAL")
                print("="*70)
                print("Review the post in the browser window")
                print("Type 'POST' to publish, or 'CANCEL' to abort: ", end='')
                approval = input().strip().upper()
                print("="*70)

                if approval == 'POST':
                    # Automated: Click Post button
                    print("\n🤖 Clicking 'Post' button...")
                    try:
                        # Try text-based selector first
                        page.click('button:has-text("Post"):not(:has-text("Start"))', timeout=5000)
                    except:
                        try:
                            # Try finding by class
                            page.click('button.share-actions__primary-action', timeout=5000)
                        except:
                            try:
                                # Try generic button near bottom
                                page.click('button[type="submit"]', timeout=5000)
                            except:
                                # Last resort: find any button with "Post" text
                                page.evaluate('Array.from(document.querySelectorAll("button")).find(b => b.textContent.includes("Post") && !b.textContent.includes("Start")).click()')

                    time.sleep(3)
                    print("\n✅ Post published successfully!")

                    # Keep browser open for verification
                    print("\n" + "="*70)
                    print("✅ POST PUBLISHED - Browser will stay open")
                    print("="*70)
                    print("You can verify the post on LinkedIn.")
                    print("Press ENTER to close browser and continue...")
                    print("="*70)
                    input()

                    context.close()
                    return True
                else:
                    print("\n❌ Post cancelled by user")
                    context.close()
                    return False

        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("\nTroubleshooting:")
            print("1. Make sure you're signed in to LinkedIn")
            print("2. Check if LinkedIn's UI has changed")
            print("3. Try running: ./install_browser_deps.sh")
            return False

    def process_approved_posts(self):
        """Process ONE approved LinkedIn post (prevents infinite loops)"""
        posts = self.find_approved_posts()

        if not posts:
            print("No approved LinkedIn posts found.")
            return

        print(f"\n📋 Found {len(posts)} approved post(s)")
        print("   Processing FIRST post only (to prevent loops)\n")

        # Process only the FIRST post
        post_file = posts[0]

        print(f"{'='*70}")
        print(f"Processing: {post_file.name}")
        print(f"{'='*70}\n")

        content = self.extract_post_content(post_file)
        success = self.post_to_linkedin_automated(content)

        if success:
            log_content = f"""---
type: linkedin_post
status: executed
executed_at: {datetime.now().isoformat()}
original_file: {post_file.name}
---

# LinkedIn Post Execution Log

## Status
✅ Successfully posted to LinkedIn

## Content Posted
{content}

## Execution Details
- Timestamp: {datetime.now().isoformat()}
- Method: Automated browser posting with HITL approval
- User sign-in: Saved in persistent profile
- Final approval: Obtained

## Original File
{post_file.name}
"""

            log_file = self.done_folder / f'EXECUTED_{post_file.name}'
            log_file.write_text(log_content, encoding='utf-8')

            done_file = self.done_folder / post_file.name
            post_file.rename(done_file)

            print(f"\n✅ Execution log saved: {log_file.name}")
            print(f"✅ Original moved to Done: {done_file.name}")
        else:
            print(f"\n⚠️ Post not published. File remains in Approved folder.")

def main():
    vault_path = Path(__file__).parent.parent / 'AI_Employee_Vault'
    poster = AutomatedLinkedInPoster(str(vault_path))
    poster.process_approved_posts()

if __name__ == '__main__':
    main()
