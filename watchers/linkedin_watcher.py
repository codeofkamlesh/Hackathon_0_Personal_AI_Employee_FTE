#!/usr/bin/env python3
"""
LinkedIn Watcher - Monitors for LinkedIn engagement opportunities
Part of Silver Tier implementation
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))
from base_watcher import BaseWatcher


class LinkedInWatcher(BaseWatcher):
    """
    Watches for LinkedIn posting opportunities based on schedule
    Creates action items for business posts to generate sales
    """

    def __init__(self, vault_path: str):
        super().__init__(vault_path, check_interval=3600)  # Check every hour

        # State file to track last post
        self.state_file = Path(__file__).parent / '.linkedin_watcher_state.json'
        self.last_post_date = None
        self._load_state()

        # Posting schedule (daily at 9 AM concept)
        self.post_frequency_hours = 24

    def _load_state(self):
        """Load last post timestamp"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                    last_post = state.get('last_post_date')
                    if last_post:
                        self.last_post_date = datetime.fromisoformat(last_post)
            except Exception as e:
                self.logger.warning(f'Could not load state: {e}')

    def _save_state(self):
        """Save last post timestamp"""
        try:
            with open(self.state_file, 'w') as f:
                state = {
                    'last_post_date': self.last_post_date.isoformat() if self.last_post_date else None
                }
                json.dump(state, f)
        except Exception as e:
            self.logger.error(f'Could not save state: {e}')

    def check_for_updates(self) -> list:
        """Check if it's time to create a LinkedIn post"""
        now = datetime.now()

        # Check if enough time has passed since last post
        if self.last_post_date:
            hours_since_last = (now - self.last_post_date).total_seconds() / 3600
            if hours_since_last < self.post_frequency_hours:
                # Not time yet
                return []

        # Time to create a post opportunity
        self.logger.info('Time to create LinkedIn post opportunity')
        return [{'type': 'linkedin_post', 'timestamp': now.isoformat()}]

    def create_action_file(self, item) -> Path:
        """Create action file for LinkedIn post opportunity"""
        try:
            now = datetime.now()

            # Create action file content
            content = f"""---
type: linkedin_post
source: linkedin_watcher
created: {now.isoformat()}
priority: medium
status: pending
requires_approval: true
---

## LinkedIn Post Opportunity

It's time to create a LinkedIn post to generate business and sales leads.

## Post Guidelines

- Focus on business value and expertise
- Share insights or recent wins
- Include a call-to-action
- Keep it professional and engaging
- Aim for 150-300 words

## Topics to Consider

- Recent project successes
- Industry insights or trends
- Tips and best practices
- Client testimonials (with permission)
- Service offerings and value proposition

## Process

1. Draft post content
2. Review for tone and accuracy
3. Move to /Pending_Approval for human review
4. After approval, post to LinkedIn

## Notes

This is an automated reminder based on your posting schedule. The actual post content should be drafted by Claude and approved by you before posting.
"""

            # Create unique filename
            timestamp = now.strftime('%Y%m%d_%H%M%S')
            filename = f'LINKEDIN_POST_{timestamp}.md'
            filepath = self.needs_action / filename

            # Write file
            filepath.write_text(content, encoding='utf-8')

            # Update last post date
            self.last_post_date = now
            self._save_state()

            self.logger.info(f'Created LinkedIn post opportunity: {filename}')
            return filepath

        except Exception as e:
            self.logger.error(f'Error creating action file: {e}')
            raise


def main():
    """Main entry point for LinkedIn watcher"""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Get vault path
    vault_path = Path(__file__).parent.parent / 'AI_Employee_Vault'

    # Create and run watcher
    watcher = LinkedInWatcher(str(vault_path))

    print(f"LinkedIn Watcher started")
    print(f"Vault: {vault_path}")
    print(f"Check interval: {watcher.check_interval} seconds")
    print(f"Post frequency: {watcher.post_frequency_hours} hours")
    print("Monitoring for LinkedIn posting opportunities...")
    print("Press Ctrl+C to stop\n")

    try:
        watcher.run()
    except KeyboardInterrupt:
        print("\nLinkedIn Watcher stopped by user")
        sys.exit(0)


if __name__ == '__main__':
    main()
