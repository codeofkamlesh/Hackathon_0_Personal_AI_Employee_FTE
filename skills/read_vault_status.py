"""
Read Vault Skill
Reads and summarizes the current state of the AI Employee vault
"""

import sys
from pathlib import Path
from datetime import datetime


def read_vault_status(vault_path: str = None):
    """
    Read and display the current status of the AI Employee vault

    Args:
        vault_path: Path to the Obsidian vault (default: AI_Employee_Vault)
    """
    if vault_path is None:
        vault_path = Path(__file__).parent.parent / 'AI_Employee_Vault'
    else:
        vault_path = Path(vault_path)

    print(f"{'='*60}")
    print(f"AI EMPLOYEE VAULT STATUS")
    print(f"{'='*60}")
    print(f"Vault Location: {vault_path.absolute()}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Check folder status
    folders = {
        'Inbox': vault_path / 'Inbox',
        'Needs_Action': vault_path / 'Needs_Action',
        'Done': vault_path / 'Done',
        'Plans': vault_path / 'Plans',
        'Pending_Approval': vault_path / 'Pending_Approval',
        'Approved': vault_path / 'Approved',
        'Rejected': vault_path / 'Rejected',
        'Logs': vault_path / 'Logs'
    }

    print("FOLDER STATUS:")
    print("-" * 60)
    for name, folder in folders.items():
        if folder.exists():
            file_count = len(list(folder.glob('*')))
            print(f"  {name:20} ✓ ({file_count} items)")
        else:
            print(f"  {name:20} ✗ (missing)")

    print()

    # Read Dashboard
    dashboard = vault_path / 'Dashboard.md'
    if dashboard.exists():
        print("DASHBOARD SUMMARY:")
        print("-" * 60)
        content = dashboard.read_text(encoding='utf-8')

        # Extract key sections
        lines = content.split('\n')
        in_summary = False
        in_activity = False

        for line in lines:
            if '## Today\'s Summary' in line:
                in_summary = True
                continue
            elif '## Recent Activity' in line:
                in_summary = False
                in_activity = True
                continue
            elif line.startswith('##'):
                in_summary = False
                in_activity = False

            if in_summary and line.strip() and not line.startswith('---'):
                print(f"  {line.strip()}")
            elif in_activity and line.strip() and not line.startswith('---') and not line.startswith('*Last'):
                print(f"  {line.strip()}")
                if in_activity:
                    break  # Only show first activity line
    else:
        print("⚠ Dashboard.md not found")

    print()

    # Check for pending actions
    needs_action = vault_path / 'Needs_Action'
    if needs_action.exists():
        action_files = list(needs_action.glob('*.md'))
        if action_files:
            print("PENDING ACTIONS:")
            print("-" * 60)
            for f in action_files[:5]:  # Show first 5
                print(f"  • {f.name}")
            if len(action_files) > 5:
                print(f"  ... and {len(action_files) - 5} more")
        else:
            print("✓ No pending actions")

    print()
    print("="*60)


if __name__ == '__main__':
    vault_path = sys.argv[1] if len(sys.argv) > 1 else None
    read_vault_status(vault_path)
