#!/bin/bash
# Automated LinkedIn Test - Fixed version

echo "=============================================="
echo "AUTOMATED LINKEDIN TEST"
echo "=============================================="
echo ""

cd "/mnt/c/Users/Admin/Documents/GitHub/Hackathon_0_Personal_AI_Employee_FTE"

# Clean up old test posts from Approved folder
echo "Cleaning up old test files..."
python3 << 'EOF'
from pathlib import Path

vault = Path('AI_Employee_Vault')
approved = vault / 'Approved'
approved.mkdir(exist_ok=True)

# Remove old test posts
for old_file in approved.glob('LINKEDIN_POST_*.md'):
    old_file.unlink()
    print(f"  Removed: {old_file.name}")

print("✅ Approved folder cleaned")
EOF

echo ""

# Create test post in Approved folder
echo "Creating test post..."
python3 << 'EOF'
from pathlib import Path
from datetime import datetime

vault = Path('AI_Employee_Vault')
approved = vault / 'Approved'
approved.mkdir(exist_ok=True)

content = f"""---
type: linkedin_post
created: {datetime.now().isoformat()}
status: approved
---

🚀 Test Post - AI Employee System

This is an automated test post to verify the LinkedIn automation is working correctly.

✅ Browser automation: Functional
✅ Form filling: Automated
✅ HITL approval: Active

#AIAutomation #Testing
"""

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filepath = approved / f'LINKEDIN_POST_{timestamp}.md'
filepath.write_text(content, encoding='utf-8')
print(f"✅ Created: {filepath.name}")
EOF

echo ""
echo "=============================================="
echo "STARTING AUTOMATED POSTING"
echo "=============================================="
echo ""
echo "📌 What will happen:"
echo "   1. Chromium browser will open"
echo "   2. LinkedIn will load"
echo "   3. Sign in if needed (saved for next time)"
echo "   4. Press ENTER after you see your feed"
echo "   5. Post will auto-compose"
echo "   6. Type 'POST' to publish"
echo "   7. Browser stays open for verification"
echo ""
echo "Press ENTER to start..."
read

# Run the poster ONCE (not in a loop)
python3 skills/automated_linkedin_poster.py

echo ""
echo "=============================================="
echo "TEST COMPLETE"
echo "=============================================="
echo ""
echo "Check AI_Employee_Vault/Done/ for execution log"
echo ""
echo "To test again, run: ./test_linkedin_auto.sh"
