"""
Process Needs Action Skill
Processes files in the Needs_Action folder and moves them to Done when complete
"""

import sys
from pathlib import Path
from datetime import datetime


def process_needs_action(vault_path: str = None):
    """
    Process all files in Needs_Action folder

    Args:
        vault_path: Path to the Obsidian vault (default: AI_Employee_Vault)
    """
    if vault_path is None:
        vault_path = Path(__file__).parent.parent / 'AI_Employee_Vault'
    else:
        vault_path = Path(vault_path)

    needs_action = vault_path / 'Needs_Action'
    done_folder = vault_path / 'Done'
    dashboard = vault_path / 'Dashboard.md'

    # Ensure folders exist
    needs_action.mkdir(parents=True, exist_ok=True)
    done_folder.mkdir(parents=True, exist_ok=True)

    # Get all files in Needs_Action
    action_files = sorted(needs_action.glob('*.md'))

    if not action_files:
        print("No files to process in Needs_Action folder")
        return

    print(f"Found {len(action_files)} file(s) to process")

    processed_count = 0

    for action_file in action_files:
        try:
            print(f"\nProcessing: {action_file.name}")

            # Read the file content
            content = action_file.read_text(encoding='utf-8')
            print(f"Content preview: {content[:200]}...")

            # Add processing timestamp
            processed_content = content + f"\n\n---\n**Processed**: {datetime.now().isoformat()}\n"

            # Move to Done folder with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            done_filename = f"{timestamp}_{action_file.name}"
            done_path = done_folder / done_filename

            done_path.write_text(processed_content, encoding='utf-8')
            action_file.unlink()  # Remove from Needs_Action

            print(f"✓ Moved to Done: {done_filename}")
            processed_count += 1

        except Exception as e:
            print(f"✗ Error processing {action_file.name}: {e}")

    # Update Dashboard
    try:
        update_dashboard(dashboard, processed_count)
    except Exception as e:
        print(f"Warning: Could not update dashboard: {e}")

    print(f"\n{'='*50}")
    print(f"Processing complete: {processed_count}/{len(action_files)} files processed")


def update_dashboard(dashboard_path: Path, processed_count: int):
    """Update the dashboard with latest activity"""
    if not dashboard_path.exists():
        return

    content = dashboard_path.read_text(encoding='utf-8')

    # Update last_updated
    content = content.replace(
        f"last_updated: {datetime.now().strftime('%Y-%m-%d')}",
        f"last_updated: {datetime.now().strftime('%Y-%m-%d')}"
    )

    # Add to recent activity
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    activity_line = f"- [{timestamp}] Processed {processed_count} file(s) from Needs_Action"

    if "## Recent Activity" in content:
        # Replace "_No activity yet_" or add to existing activity
        if "_No activity yet_" in content:
            content = content.replace("_No activity yet_", activity_line)
        else:
            # Add after "## Recent Activity"
            content = content.replace(
                "## Recent Activity\n",
                f"## Recent Activity\n{activity_line}\n"
            )

    dashboard_path.write_text(content, encoding='utf-8')


if __name__ == '__main__':
    vault_path = sys.argv[1] if len(sys.argv) > 1 else None
    process_needs_action(vault_path)
