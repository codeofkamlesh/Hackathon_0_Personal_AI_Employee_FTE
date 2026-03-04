#!/usr/bin/env python3
"""
LinkedIn Poster - Posts approved content to LinkedIn using browser automation
Part of Silver Tier - Actual posting functionality
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
import time

class LinkedInPoster:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.approved_folder = self.vault_path / 'Approved'
        self.done_folder = self.vault_path / 'Done'
        self.playwright_script = Path(__file__).parent.parent / '.claude' / 'skills' / 'browsing-with-playwright' / 'scripts'

    def find_approved_posts(self):
        """Find approved LinkedIn posts"""
        posts = list(self.approved_folder.glob('LINKEDIN_POST_*.md'))
        return posts

    def extract_post_content(self, filepath: Path):
        """Extract post content from markdown file"""
        content = filepath.read_text(encoding='utf-8')

        # Extract content between frontmatter
        lines = content.split('\n')
        in_content = False
        post_lines = []

        for line in lines:
            if line.strip() == '---' and not in_content:
                in_content = True
                continue
            if line.strip() == '---' and in_content:
                in_content = False
                continue
            if not in_content and line.strip() and not line.startswith('#'):
                post_lines.append(line)

        return '\n'.join(post_lines).strip()

    def post_to_linkedin(self, content: str):
        """
        Post content to LinkedIn using Playwright browser automation
        Opens browser for user authentication
        """
        print("\n" + "="*60)
        print("LINKEDIN POSTING - Browser Automation")
        print("="*60)
        print("\n📝 Content to post:")
        print("-" * 60)
        print(content)
        print("-" * 60)

        print("\n🌐 Opening LinkedIn in browser...")
        print("👤 Please sign in to your LinkedIn account when prompted")
        print("⏳ Waiting for authentication...")

        # Start Playwright MCP server
        print("\n🚀 Starting browser automation server...")
        start_cmd = f"bash {self.playwright_script}/start-server.sh"
        subprocess.run(start_cmd, shell=True, check=False)
        time.sleep(3)

        try:
            # Navigate to LinkedIn
            print("\n1️⃣ Navigating to LinkedIn...")
            nav_cmd = f"""python3 {self.playwright_script}/mcp-client.py call -u http://localhost:8808 -t browser_navigate -p '{{"url": "https://www.linkedin.com"}}'"""
            subprocess.run(nav_cmd, shell=True, check=True)
            time.sleep(2)

            print("\n✋ MANUAL STEP REQUIRED:")
            print("   1. Sign in to LinkedIn in the browser window")
            print("   2. Navigate to your home feed")
            print("   3. Press ENTER here when ready to post...")
            input()

            # Get page snapshot to find post button
            print("\n2️⃣ Finding 'Start a post' button...")
            snapshot_cmd = f"""python3 {self.playwright_script}/mcp-client.py call -u http://localhost:8808 -t browser_snapshot -p '{{}}'"""
            result = subprocess.run(snapshot_cmd, shell=True, capture_output=True, text=True)

            # Click "Start a post" button
            print("\n3️⃣ Clicking 'Start a post'...")
            click_cmd = f"""python3 {self.playwright_script}/mcp-client.py call -u http://localhost:8808 -t browser_click -p '{{"element": "Start a post"}}'"""
            subprocess.run(click_cmd, shell=True, check=False)
            time.sleep(2)

            # Type the post content
            print("\n4️⃣ Typing post content...")
            # Escape content for JSON
            escaped_content = content.replace('"', '\\"').replace('\n', '\\n')
            type_cmd = f"""python3 {self.playwright_script}/mcp-client.py call -u http://localhost:8808 -t browser_type -p '{{"element": "post text", "text": "{escaped_content}"}}'"""
            subprocess.run(type_cmd, shell=True, check=False)
            time.sleep(1)

            print("\n✋ FINAL APPROVAL:")
            print("   Review the post in the browser")
            print("   Type 'POST' to publish, or 'CANCEL' to abort: ", end='')
            approval = input().strip().upper()

            if approval == 'POST':
                # Click Post button
                print("\n5️⃣ Publishing post...")
                post_cmd = f"""python3 {self.playwright_script}/mcp-client.py call -u http://localhost:8808 -t browser_click -p '{{"element": "Post"}}'"""
                subprocess.run(post_cmd, shell=True, check=False)
                time.sleep(3)

                print("\n✅ Post published successfully!")
                return True
            else:
                print("\n❌ Post cancelled by user")
                return False

        except Exception as e:
            print(f"\n❌ Error during posting: {e}")
            return False
        finally:
            # Stop Playwright server
            print("\n🛑 Closing browser...")
            stop_cmd = f"bash {self.playwright_script}/stop-server.sh"
            subprocess.run(stop_cmd, shell=True, check=False)

    def process_approved_posts(self):
        """Process all approved LinkedIn posts"""
        posts = self.find_approved_posts()

        if not posts:
            print("No approved LinkedIn posts found.")
            return

        print(f"\n📋 Found {len(posts)} approved post(s)")

        for post_file in posts:
            print(f"\n{'='*60}")
            print(f"Processing: {post_file.name}")
            print(f"{'='*60}")

            # Extract content
            content = self.extract_post_content(post_file)

            # Post to LinkedIn
            success = self.post_to_linkedin(content)

            if success:
                # Create execution log
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
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
- Method: Browser automation (Playwright)
- User approval: Required and obtained

## Original File
{post_file.name}
"""

                # Save execution log
                log_file = self.done_folder / f'EXECUTED_{post_file.name}'
                log_file.write_text(log_content, encoding='utf-8')

                # Move original to Done
                done_file = self.done_folder / post_file.name
                post_file.rename(done_file)

                print(f"\n✅ Execution log saved: {log_file.name}")
                print(f"✅ Original moved to Done: {done_file.name}")
            else:
                print(f"\n⚠️ Post not published. File remains in Approved folder.")

def main():
    """Main entry point"""
    vault_path = Path(__file__).parent.parent / 'AI_Employee_Vault'
    poster = LinkedInPoster(str(vault_path))
    poster.process_approved_posts()

if __name__ == '__main__':
    main()
