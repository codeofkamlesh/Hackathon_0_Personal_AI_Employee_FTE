#!/usr/bin/env python3
"""
Silver Tier Validation Script
Verifies all Silver Tier components are present and functional
"""

import sys
from pathlib import Path
from datetime import datetime
import json


class SilverTierValidator:
    """Validates Silver Tier implementation"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.vault_path = self.project_root / 'AI_Employee_Vault'
        self.results = []
        self.passed = 0
        self.failed = 0

    def test(self, name: str, condition: bool, details: str = ""):
        """Record test result"""
        status = "✓ PASS" if condition else "✗ FAIL"
        self.results.append(f"{status}: {name}")
        if details:
            self.results.append(f"        {details}")

        if condition:
            self.passed += 1
        else:
            self.failed += 1

        return condition

    def validate_bronze_requirements(self):
        """Verify Bronze tier is still intact"""
        print("\n" + "=" * 60)
        print("BRONZE TIER VALIDATION (Prerequisites)")
        print("=" * 60)

        # Vault structure
        self.test(
            "Obsidian vault exists",
            self.vault_path.exists(),
            str(self.vault_path)
        )

        # Core folders
        folders = ['Inbox', 'Needs_Action', 'Done', 'Plans', 'Pending_Approval', 'Approved', 'Rejected', 'Logs']
        for folder in folders:
            folder_path = self.vault_path / folder
            self.test(
                f"Folder: {folder}",
                folder_path.exists(),
                str(folder_path)
            )

        # Core files
        self.test(
            "Dashboard.md exists",
            (self.vault_path / 'Dashboard.md').exists()
        )

        self.test(
            "Company_Handbook.md exists",
            (self.vault_path / 'Company_Handbook.md').exists()
        )

        # Bronze watcher
        self.test(
            "Base watcher exists",
            (self.project_root / 'watchers' / 'base_watcher.py').exists()
        )

        self.test(
            "Filesystem watcher exists",
            (self.project_root / 'watchers' / 'filesystem_watcher.py').exists()
        )

    def validate_silver_watchers(self):
        """Verify Silver tier watchers"""
        print("\n" + "=" * 60)
        print("SILVER TIER: MULTIPLE WATCHERS")
        print("=" * 60)

        # Gmail watcher
        gmail_watcher = self.project_root / 'watchers' / 'gmail_watcher.py'
        self.test(
            "Gmail watcher exists",
            gmail_watcher.exists(),
            str(gmail_watcher)
        )

        if gmail_watcher.exists():
            content = gmail_watcher.read_text()
            self.test(
                "Gmail watcher has GmailWatcher class",
                'class GmailWatcher' in content
            )
            self.test(
                "Gmail watcher has check_for_updates method",
                'def check_for_updates' in content
            )

        # LinkedIn watcher
        linkedin_watcher = self.project_root / 'watchers' / 'linkedin_watcher.py'
        self.test(
            "LinkedIn watcher exists",
            linkedin_watcher.exists(),
            str(linkedin_watcher)
        )

        if linkedin_watcher.exists():
            content = linkedin_watcher.read_text()
            self.test(
                "LinkedIn watcher has LinkedInWatcher class",
                'class LinkedInWatcher' in content
            )
            self.test(
                "LinkedIn watcher has posting schedule logic",
                'post_frequency_hours' in content
            )

    def validate_reasoning_loop(self):
        """Verify reasoning loop implementation"""
        print("\n" + "=" * 60)
        print("SILVER TIER: REASONING LOOP")
        print("=" * 60)

        reasoning_loop = self.project_root / 'skills' / 'reasoning_loop.py'
        self.test(
            "Reasoning loop script exists",
            reasoning_loop.exists(),
            str(reasoning_loop)
        )

        if reasoning_loop.exists():
            content = reasoning_loop.read_text()
            self.test(
                "Reasoning loop reads Needs_Action",
                'read_needs_action' in content
            )
            self.test(
                "Reasoning loop generates plans",
                'generate_plan' in content
            )
            self.test(
                "Reasoning loop handles email plans",
                'generate_email_plan' in content
            )
            self.test(
                "Reasoning loop handles LinkedIn plans",
                'generate_linkedin_plan' in content
            )

        # Check for SKILL.md
        skill_md = self.project_root / 'skills' / 'reasoning_loop' / 'SKILL.md'
        self.test(
            "Reasoning loop SKILL.md exists",
            skill_md.exists(),
            str(skill_md)
        )

    def validate_hitl_workflow(self):
        """Verify Human-in-the-Loop workflow"""
        print("\n" + "=" * 60)
        print("SILVER TIER: HUMAN-IN-THE-LOOP (HITL)")
        print("=" * 60)

        # LinkedIn drafter with HITL
        linkedin_drafter = self.project_root / 'skills' / 'linkedin_drafter.py'
        self.test(
            "LinkedIn drafter exists",
            linkedin_drafter.exists(),
            str(linkedin_drafter)
        )

        if linkedin_drafter.exists():
            content = linkedin_drafter.read_text()
            self.test(
                "LinkedIn drafter creates approval requests",
                'create_approval_request' in content
            )
            self.test(
                "LinkedIn drafter checks approved posts",
                'check_approved_posts' in content
            )
            self.test(
                "LinkedIn drafter executes approved posts",
                'execute_approved_post' in content
            )
            self.test(
                "LinkedIn drafter uses Pending_Approval folder",
                'Pending_Approval' in content
            )

        # Check for SKILL.md
        skill_md = self.project_root / 'skills' / 'linkedin_drafter' / 'SKILL.md'
        self.test(
            "LinkedIn drafter SKILL.md exists",
            skill_md.exists(),
            str(skill_md)
        )

        # Verify approval folders exist
        self.test(
            "Pending_Approval folder exists",
            (self.vault_path / 'Pending_Approval').exists()
        )
        self.test(
            "Approved folder exists",
            (self.vault_path / 'Approved').exists()
        )
        self.test(
            "Rejected folder exists",
            (self.vault_path / 'Rejected').exists()
        )

    def validate_mcp_server(self):
        """Verify MCP server implementation"""
        print("\n" + "=" * 60)
        print("SILVER TIER: EMAIL MCP SERVER")
        print("=" * 60)

        mcp_dir = self.project_root / 'mcp-servers' / 'email'
        self.test(
            "MCP email directory exists",
            mcp_dir.exists(),
            str(mcp_dir)
        )

        # Check index.js
        index_js = mcp_dir / 'index.js'
        self.test(
            "MCP server index.js exists",
            index_js.exists(),
            str(index_js)
        )

        if index_js.exists():
            content = index_js.read_text()
            self.test(
                "MCP server has EmailMCPServer class",
                'class EmailMCPServer' in content
            )
            self.test(
                "MCP server has send_email tool",
                'send_email' in content
            )
            self.test(
                "MCP server has draft_email tool",
                'draft_email' in content
            )

        # Check package.json
        package_json = mcp_dir / 'package.json'
        self.test(
            "MCP server package.json exists",
            package_json.exists(),
            str(package_json)
        )

        if package_json.exists():
            try:
                data = json.loads(package_json.read_text())
                self.test(
                    "package.json has MCP SDK dependency",
                    '@modelcontextprotocol/sdk' in data.get('dependencies', {})
                )
                self.test(
                    "package.json has nodemailer dependency",
                    'nodemailer' in data.get('dependencies', {})
                )
            except:
                self.test("package.json is valid JSON", False)

        # Check README
        readme = mcp_dir / 'README.md'
        self.test(
            "MCP server README.md exists",
            readme.exists(),
            str(readme)
        )

    def validate_scheduling(self):
        """Verify scheduling configuration"""
        print("\n" + "=" * 60)
        print("SILVER TIER: SCHEDULING")
        print("=" * 60)

        cron_file = self.project_root / 'cron_schedule.txt'
        self.test(
            "Cron schedule file exists",
            cron_file.exists(),
            str(cron_file)
        )

        if cron_file.exists():
            content = cron_file.read_text()
            self.test(
                "Cron schedule includes Gmail watcher",
                'gmail_watcher.py' in content
            )
            self.test(
                "Cron schedule includes LinkedIn watcher",
                'linkedin_watcher.py' in content
            )
            self.test(
                "Cron schedule includes reasoning loop",
                'reasoning_loop.py' in content
            )
            self.test(
                "Cron schedule includes daily briefing",
                'briefing' in content.lower()
            )

    def validate_agent_skills(self):
        """Verify all AI functionality is implemented as Agent Skills"""
        print("\n" + "=" * 60)
        print("SILVER TIER: AGENT SKILLS")
        print("=" * 60)

        skills_dir = self.project_root / 'skills'
        self.test(
            "Skills directory exists",
            skills_dir.exists(),
            str(skills_dir)
        )

        # Check for SKILL.md files
        expected_skills = [
            'read_vault_status',
            'process_needs_action',
            'reasoning_loop',
            'linkedin_drafter'
        ]

        for skill in expected_skills:
            skill_md = skills_dir / skill / 'SKILL.md'
            if not skill_md.exists():
                # Try without subdirectory
                skill_md = skills_dir / f'{skill}' / 'SKILL.md'

            self.test(
                f"Agent Skill: {skill}",
                skill_md.exists() or (skills_dir / f'{skill}.py').exists(),
                f"Looking for SKILL.md or .py file"
            )

    def validate_functional_tests(self):
        """Run functional tests"""
        print("\n" + "=" * 60)
        print("FUNCTIONAL TESTS")
        print("=" * 60)

        # Test reasoning loop can be imported
        try:
            sys.path.insert(0, str(self.project_root / 'skills'))
            import reasoning_loop
            self.test(
                "Reasoning loop can be imported",
                True
            )
        except Exception as e:
            self.test(
                "Reasoning loop can be imported",
                False,
                str(e)
            )

        # Test LinkedIn drafter can be imported
        try:
            import linkedin_drafter
            self.test(
                "LinkedIn drafter can be imported",
                True
            )
        except Exception as e:
            self.test(
                "LinkedIn drafter can be imported",
                False,
                str(e)
            )

        # Test watchers can be imported
        try:
            sys.path.insert(0, str(self.project_root / 'watchers'))
            import gmail_watcher
            self.test(
                "Gmail watcher can be imported",
                True
            )
        except Exception as e:
            self.test(
                "Gmail watcher can be imported",
                False,
                str(e)
            )

        try:
            import linkedin_watcher
            self.test(
                "LinkedIn watcher can be imported",
                True
            )
        except Exception as e:
            self.test(
                "LinkedIn watcher can be imported",
                False,
                str(e)
            )

    def run(self):
        """Run all validation tests"""
        print("\n" + "=" * 60)
        print("SILVER TIER VALIDATION")
        print("Personal AI Employee - Hackathon 0")
        print("=" * 60)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(f"Project Root: {self.project_root}")

        # Run all validation categories
        self.validate_bronze_requirements()
        self.validate_silver_watchers()
        self.validate_reasoning_loop()
        self.validate_hitl_workflow()
        self.validate_mcp_server()
        self.validate_scheduling()
        self.validate_agent_skills()
        self.validate_functional_tests()

        # Print summary
        print("\n" + "=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)
        print(f"Tests Passed: {self.passed}")
        print(f"Tests Failed: {self.failed}")
        print(f"Total Tests: {self.passed + self.failed}")
        print(f"Success Rate: {(self.passed / (self.passed + self.failed) * 100):.1f}%")

        if self.failed == 0:
            print("\n🎉 SILVER TIER VALIDATION PASSED!")
            print("All components are present and functional.")
            return 0
        else:
            print(f"\n⚠ SILVER TIER VALIDATION INCOMPLETE")
            print(f"{self.failed} test(s) failed. Review the output above.")
            return 1


def main():
    """Main entry point"""
    validator = SilverTierValidator()
    exit_code = validator.run()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
