#!/bin/bash
# Simple LinkedIn Test - Opens REAL browser window

echo "=============================================="
echo "LINKEDIN TEST - Real Browser Window"
echo "=============================================="
echo ""

PROJECT_DIR="/mnt/c/Users/Admin/Documents/GitHub/Hackathon_0_Personal_AI_Employee_FTE"
cd "$PROJECT_DIR"

# Step 1: Create test post in Approved folder (skip drafting for quick test)
echo "Step 1: Creating test LinkedIn post..."
echo "-----------------------------------------------"
./venv/bin/python3 << 'EOF'
from pathlib import Path
from datetime import datetime

vault = Path('AI_Employee_Vault')
approved = vault / 'Approved'

content = f"""---
type: linkedin_post
source: test_script
created: {datetime.now().isoformat()}
status: approved
---

🚀 Test Post from AI Employee System

This is a test post to verify the LinkedIn automation is working correctly.

✅ System is operational
✅ Browser automation functional
✅ Ready for production use

#AIAutomation #Testing #TechInnovation
"""

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f'LINKEDIN_POST_{timestamp}.md'
filepath = approved / filename

filepath.write_text(content, encoding='utf-8')
print(f"✅ Created: {filename}")
print(f"📁 Location: {filepath}")
EOF

echo ""
echo "Step 2: Opening browser for LinkedIn posting..."
echo "-----------------------------------------------"
echo "🌐 Browser will open in 3 seconds..."
sleep 3

./venv/bin/python3 skills/simple_linkedin_poster.py

echo ""
echo "=============================================="
echo "TEST COMPLETE"
echo "=============================================="
echo ""
echo "Check AI_Employee_Vault/Done/ for execution log"
