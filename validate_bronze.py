#!/usr/bin/env python3
"""
Bronze Tier Validation Script
Verifies that all Bronze tier requirements are met
"""

import sys
from pathlib import Path


def validate_bronze_tier():
    """Validate all Bronze tier requirements"""

    print("=" * 60)
    print("BRONZE TIER VALIDATION")
    print("=" * 60)
    print()

    project_root = Path(__file__).parent
    vault_path = project_root / 'AI_Employee_Vault'

    all_checks_passed = True

    # Check 1: Vault structure
    print("✓ Checking vault structure...")
    required_folders = [
        'Inbox', 'Needs_Action', 'Done', 'Plans',
        'Pending_Approval', 'Approved', 'Rejected', 'Logs'
    ]

    for folder in required_folders:
        folder_path = vault_path / folder
        if folder_path.exists():
            print(f"  ✓ {folder}/ exists")
        else:
            print(f"  ✗ {folder}/ missing")
            all_checks_passed = False

    print()

    # Check 2: Core markdown files
    print("✓ Checking core markdown files...")
    required_files = ['Dashboard.md', 'Company_Handbook.md']

    for file in required_files:
        file_path = vault_path / file
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"  ✓ {file} exists ({size} bytes)")
        else:
            print(f"  ✗ {file} missing")
            all_checks_passed = False

    print()

    # Check 3: Watcher scripts
    print("✓ Checking watcher scripts...")
    watcher_files = ['base_watcher.py', 'filesystem_watcher.py']
    watchers_path = project_root / 'watchers'

    for file in watcher_files:
        file_path = watchers_path / file
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"  ✓ {file} exists ({size} bytes)")
        else:
            print(f"  ✗ {file} missing")
            all_checks_passed = False

    print()

    # Check 4: Agent Skills
    print("✓ Checking agent skills...")
    skill_files = ['read_vault_status.py', 'process_needs_action.py']
    skills_path = project_root / 'skills'

    for file in skill_files:
        file_path = skills_path / file
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"  ✓ {file} exists ({size} bytes)")

            # Check for SKILL.md
            skill_name = file.replace('.py', '')
            skill_md = skills_path / skill_name / 'SKILL.md'
            if skill_md.exists():
                print(f"    ✓ {skill_name}/SKILL.md exists")
            else:
                print(f"    ✗ {skill_name}/SKILL.md missing")
                all_checks_passed = False
        else:
            print(f"  ✗ {file} missing")
            all_checks_passed = False

    print()

    # Check 5: Documentation
    print("✓ Checking documentation...")
    doc_files = ['README.md', 'DEMO.md', 'STATUS.md']

    for file in doc_files:
        file_path = project_root / file
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"  ✓ {file} exists ({size} bytes)")
        else:
            print(f"  ✗ {file} missing")
            all_checks_passed = False

    print()

    # Check 6: Test functionality
    print("✓ Testing functionality...")

    # Test read_vault_status
    try:
        sys.path.insert(0, str(skills_path))
        from read_vault_status import read_vault_status
        print("  ✓ read_vault_status skill can be imported")
    except Exception as e:
        print(f"  ✗ read_vault_status import failed: {e}")
        all_checks_passed = False

    # Test process_needs_action
    try:
        from process_needs_action import process_needs_action
        print("  ✓ process_needs_action skill can be imported")
    except Exception as e:
        print(f"  ✗ process_needs_action import failed: {e}")
        all_checks_passed = False

    print()
    print("=" * 60)

    if all_checks_passed:
        print("✓ ALL BRONZE TIER REQUIREMENTS MET")
        print()
        print("Your Bronze tier implementation is complete!")
        print("You can now:")
        print("  1. Start the watcher: cd watchers && python3 filesystem_watcher.py")
        print("  2. Drop files in Inbox to test")
        print("  3. Use Claude Code to process tasks")
        print("  4. Upgrade to Silver tier")
        return 0
    else:
        print("✗ SOME REQUIREMENTS NOT MET")
        print()
        print("Please review the errors above and fix missing components.")
        return 1


if __name__ == '__main__':
    sys.exit(validate_bronze_tier())
