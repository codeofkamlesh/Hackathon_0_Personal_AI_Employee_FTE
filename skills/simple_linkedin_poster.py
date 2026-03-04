#!/usr/bin/env python3
"""
Simple LinkedIn Poster - Opens real browser for posting
Uses Playwright directly (no MCP server needed)
"""

import sys
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright
import time

class SimpleLinkedInPoster:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.approved_folder = self.vault_path / 'Approved'
        self.done_folder = self.vault_path / 'Done'

    def find_approved_posts(self):
        """Find approved LinkedIn posts"""
        return list(self.approved_folder.glob('LINKEDIN_POST_*.md'))

    def extract_post_content(self, filepath: Path):
        """Extract post content from markdown file"""
        content = filepath.read_text(encoding='utf-8')
        lines = content.split('\n')

        # Skip frontmatter and extract main content
        in_frontmatter = False
        post_lines = []

        for line in lines:
            if line.strip() == '---':
                in_frontmatter = not in_frontmatter
                continue
            if not in_frontmatter and line.strip() and not line.startswith('#'):
                # Skip checklist items
                if not line.strip().startswith('- ['):
                    post_lines.append(line)

        return '\n'.join(post_lines).strip()

    def post_to_linkedin(self, content: str):
        """
        Post to LinkedIn using Playwright
        Opens REAL browser window for user interaction
        """
        print("\n" + "="*70)
        print("LINKEDIN POSTING - Real Browser Window")
        print("="*70)
        print("\n📝 Content to post:")
        print("-" * 70)
        print(content)
        print("-" * 70)

        print("\n🌐 Opening LinkedIn in browser...")
        print("👤 You will sign in and post manually")
        print("")

        try:
            with sync_playwright() as p:
                # Launch browser in NON-HEADLESS mode (visible window)
                print("🚀 Launching browser...")
                browser = p.chromium.launch(headless=False, slow_mo=1000)
                context = browser.new_context()
                page = context.new_page()

                # Navigate to LinkedIn
                print("📱 Opening LinkedIn...")
                page.goto('https://www.linkedin.com')

                print("\n" + "="*70)
                print("MANUAL STEPS - Follow these in the browser:")
                print("="*70)
                print("1. Sign in to your LinkedIn account")
                print("2. Click 'Start a post' button")
                print("3. Copy the content shown above")
                print("4. Paste it into the post box")
                print("5. Click 'Post' button")
                print("="*70)
                print("\nPress ENTER here after you've posted...")

                input()

                print("\n✅ Post completed!")

                browser.close()
                return True

        except Exception as e:
            print(f"\n❌ Error: {e}")
            return False

    def process_approved_posts(self):
        """Process all approved LinkedIn posts"""
        posts = self.find_approved_posts()

        if not posts:
            print("No approved LinkedIn posts found.")
            return

        print(f"\n📋 Found {len(posts)} approved post(s)\n")

        for post_file in posts:
            print(f"{'='*70}")
            print(f"Processing: {post_file.name}")
            print(f"{'='*70}\n")

            # Extract content
            content = self.extract_post_content(post_file)

            # Post to LinkedIn
            success = self.post_to_linkedin(content)

            if success:
                # Create execution log
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
- Method: Manual posting via browser
- User confirmation: Obtained

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
                print(f"\n⚠️ Post not completed. File remains in Approved folder.")

def main():
    """Main entry point"""
    vault_path = Path(__file__).parent.parent / 'AI_Employee_Vault'
    poster = SimpleLinkedInPoster(str(vault_path))
    poster.process_approved_posts()

if __name__ == '__main__':
    main()
