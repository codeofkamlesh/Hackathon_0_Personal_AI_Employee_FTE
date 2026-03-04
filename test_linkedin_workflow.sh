#!/bin/bash
# Complete LinkedIn Workflow Test
# Tests: Watcher → Drafter → Approval → Posting

echo "=============================================="
echo "LINKEDIN WORKFLOW - COMPLETE TEST"
echo "=============================================="
echo ""

PROJECT_DIR="/mnt/c/Users/Admin/Documents/GitHub/Hackathon_0_Personal_AI_Employee_FTE"
cd "$PROJECT_DIR"

# Step 1: Create a LinkedIn posting opportunity
echo "Step 1: Creating LinkedIn posting opportunity..."
echo "-----------------------------------------------"
./venv/bin/python3 << 'EOF'
from pathlib import Path
from datetime import datetime

vault = Path('AI_Employee_Vault')
needs_action = vault / 'Needs_Action'

content = f"""---
type: linkedin_post
source: test_script
created: {datetime.now().isoformat()}
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

## Process

1. Draft post content
2. Review for tone and accuracy
3. Move to /Pending_Approval for human review
4. After approval, post to LinkedIn
"""

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f'LINKEDIN_POST_{timestamp}.md'
filepath = needs_action / filename

filepath.write_text(content, encoding='utf-8')
print(f"✅ Created: {filename}")
EOF

echo ""
echo "Step 2: Drafting LinkedIn post..."
echo "-----------------------------------------------"
./venv/bin/python3 skills/linkedin_drafter.py

echo ""
echo "Step 3: Review the draft..."
echo "-----------------------------------------------"
echo "📁 Check: AI_Employee_Vault/Pending_Approval/"
ls -lh AI_Employee_Vault/Pending_Approval/LINKEDIN_POST_*.md 2>/dev/null | tail -1

echo ""
echo "✋ MANUAL STEP:"
echo "   1. Open the file in Pending_Approval/"
echo "   2. Review and edit the post content if needed"
echo "   3. Move the file to Approved/ folder"
echo ""
read -p "Press ENTER when you've moved the file to Approved/..."

echo ""
echo "Step 4: Posting to LinkedIn..."
echo "-----------------------------------------------"
echo "🌐 Browser will open for LinkedIn authentication"
echo "👤 You'll need to sign in to LinkedIn"
echo ""
./venv/bin/python3 skills/linkedin_poster.py

echo ""
echo "=============================================="
echo "LINKEDIN WORKFLOW TEST COMPLETE"
echo "=============================================="
echo ""
echo "Check AI_Employee_Vault/Done/ for execution logs"
