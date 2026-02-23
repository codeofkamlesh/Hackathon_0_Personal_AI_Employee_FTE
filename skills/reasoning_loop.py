#!/usr/bin/env python3
"""
Reasoning Loop - Reads Needs_Action and generates Plan.md files
Part of Silver Tier implementation
"""

import sys
from pathlib import Path
from datetime import datetime
import json


def read_needs_action(vault_path: Path) -> list:
    """Read all files from Needs_Action folder"""
    needs_action = vault_path / 'Needs_Action'

    if not needs_action.exists():
        return []

    action_files = list(needs_action.glob('*.md'))
    return action_files


def parse_action_file(filepath: Path) -> dict:
    """Parse action file and extract metadata"""
    try:
        content = filepath.read_text(encoding='utf-8')

        # Extract frontmatter
        metadata = {}
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1].strip()
                for line in frontmatter.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        metadata[key.strip()] = value.strip()

        return {
            'filepath': filepath,
            'filename': filepath.name,
            'metadata': metadata,
            'content': content
        }
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        return None


def generate_plan(action_item: dict, vault_path: Path) -> Path:
    """Generate a Plan.md file for an action item"""
    plans_folder = vault_path / 'Plans'
    plans_folder.mkdir(exist_ok=True)

    metadata = action_item['metadata']
    action_type = metadata.get('type', 'unknown')

    # Generate plan based on action type
    if action_type == 'email':
        plan_content = generate_email_plan(action_item)
    elif action_type == 'linkedin_post':
        plan_content = generate_linkedin_plan(action_item)
    elif action_type == 'file_drop':
        plan_content = generate_file_plan(action_item)
    else:
        plan_content = generate_generic_plan(action_item)

    # Create plan filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_name = action_item['filename'].replace('.md', '')
    plan_filename = f'PLAN_{timestamp}_{base_name}.md'
    plan_path = plans_folder / plan_filename

    # Write plan file
    plan_path.write_text(plan_content, encoding='utf-8')

    return plan_path


def generate_email_plan(action_item: dict) -> str:
    """Generate plan for email action"""
    metadata = action_item['metadata']

    return f"""---
type: plan
source: reasoning_loop
action_type: email
created: {datetime.now().isoformat()}
status: pending
original_file: {action_item['filename']}
---

# Plan: Process Email

## Context

- **From**: {metadata.get('from', 'Unknown')}
- **Subject**: {metadata.get('subject', 'No subject')}
- **Priority**: {metadata.get('priority', 'normal')}

## Objective

Process the incoming email and determine appropriate response.

## Steps

- [ ] Read and understand the email content
- [ ] Identify the sender's intent and any requests
- [ ] Determine if a response is needed
- [ ] Draft response if required (requires approval)
- [ ] Check Company_Handbook.md for relevant policies
- [ ] Move to appropriate folder when complete

## Decision Points

1. **Response Required?**
   - If yes: Draft reply and move to /Pending_Approval
   - If no: Archive to /Done with summary

2. **Urgency Level**
   - High: Process immediately
   - Medium: Process within 24 hours
   - Low: Process within 48 hours

## Next Actions

Review the original email file and execute the plan steps.
"""


def generate_linkedin_plan(action_item: dict) -> str:
    """Generate plan for LinkedIn post"""
    return f"""---
type: plan
source: reasoning_loop
action_type: linkedin_post
created: {datetime.now().isoformat()}
status: pending
original_file: {action_item['filename']}
---

# Plan: Create LinkedIn Post

## Objective

Draft a professional LinkedIn post to generate business leads and showcase expertise.

## Steps

- [ ] Review Company_Handbook.md for brand voice and guidelines
- [ ] Identify recent wins or insights to share
- [ ] Draft post content (150-300 words)
- [ ] Include relevant hashtags
- [ ] Add call-to-action
- [ ] Create approval request in /Pending_Approval
- [ ] Wait for human approval before posting

## Content Guidelines

1. **Tone**: Professional, confident, helpful
2. **Focus**: Value proposition and expertise
3. **Structure**: Hook → Value → Call-to-action
4. **Length**: 150-300 words optimal

## Topics to Consider

- Recent project successes
- Industry insights
- Client testimonials
- Service offerings
- Tips and best practices

## Approval Required

This action requires human approval before execution. Draft will be placed in /Pending_Approval.

## Next Actions

1. Draft the LinkedIn post content
2. Create approval request file
3. Wait for approval
4. Execute post (via MCP or manual)
"""


def generate_file_plan(action_item: dict) -> str:
    """Generate plan for file drop"""
    metadata = action_item['metadata']

    return f"""---
type: plan
source: reasoning_loop
action_type: file_processing
created: {datetime.now().isoformat()}
status: pending
original_file: {action_item['filename']}
---

# Plan: Process Dropped File

## Context

- **File**: {metadata.get('original_name', 'Unknown')}
- **Size**: {metadata.get('size', 'Unknown')} bytes
- **Type**: {metadata.get('type', 'file_drop')}

## Objective

Process the dropped file and determine appropriate action.

## Steps

- [ ] Identify file type and purpose
- [ ] Read file contents if text-based
- [ ] Determine processing requirements
- [ ] Execute appropriate action
- [ ] Log results
- [ ] Move to /Done when complete

## Decision Points

1. **File Type**
   - Document: Review and summarize
   - Data: Process and analyze
   - Image: Catalog and describe
   - Other: Determine handling

2. **Action Required**
   - Store for reference
   - Process and extract data
   - Forward to external system
   - Archive

## Next Actions

Examine the file and execute the appropriate processing steps.
"""


def generate_generic_plan(action_item: dict) -> str:
    """Generate generic plan for unknown action types"""
    return f"""---
type: plan
source: reasoning_loop
action_type: generic
created: {datetime.now().isoformat()}
status: pending
original_file: {action_item['filename']}
---

# Plan: Process Action Item

## Context

Action item detected that requires processing.

## Objective

Review the action item and determine appropriate steps.

## Steps

- [ ] Read and understand the action item
- [ ] Identify required actions
- [ ] Check for dependencies or prerequisites
- [ ] Execute actions in appropriate order
- [ ] Log results
- [ ] Move to /Done when complete

## Next Actions

Review the original action file and determine specific steps needed.
"""


def main():
    """Main entry point for reasoning loop"""
    # Get vault path
    vault_path = Path(__file__).parent.parent / 'AI_Employee_Vault'

    if not vault_path.exists():
        print(f"Error: Vault not found at {vault_path}")
        sys.exit(1)

    print("Reasoning Loop - Plan Generation")
    print("=" * 50)
    print(f"Vault: {vault_path}\n")

    # Read action items
    action_files = read_needs_action(vault_path)

    if not action_files:
        print("No action items found in Needs_Action folder.")
        return

    print(f"Found {len(action_files)} action item(s)\n")

    # Generate plans for each action item
    plans_created = 0
    for action_file in action_files:
        print(f"Processing: {action_file.name}")

        # Parse action file
        action_item = parse_action_file(action_file)
        if not action_item:
            print(f"  ⚠ Could not parse file")
            continue

        # Generate plan
        try:
            plan_path = generate_plan(action_item, vault_path)
            print(f"  ✓ Plan created: {plan_path.name}")
            plans_created += 1
        except Exception as e:
            print(f"  ✗ Error creating plan: {e}")

    print(f"\n{'=' * 50}")
    print(f"Plans created: {plans_created}/{len(action_files)}")


if __name__ == '__main__':
    main()
