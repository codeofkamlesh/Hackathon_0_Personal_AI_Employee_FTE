#!/bin/bash
# Complete Gmail Workflow Test
# Tests: Watcher → Drafter → Approval → Reply Sending

echo "=============================================="
echo "GMAIL WORKFLOW - COMPLETE TEST"
echo "=============================================="
echo ""

PROJECT_DIR="/mnt/c/Users/Admin/Documents/GitHub/Hackathon_0_Personal_AI_Employee_FTE"
cd "$PROJECT_DIR"

# Step 1: Check Gmail authentication
echo "Step 1: Checking Gmail authentication..."
echo "-----------------------------------------------"
if [ ! -f "token.pickle" ]; then
    echo "⚠️  Gmail not authenticated yet"
    echo "Running first-time authentication..."
    ./venv/bin/python3 watchers/gmail_watcher.py &
    WATCHER_PID=$!
    echo ""
    echo "✋ Please complete authentication in the browser"
    echo "   Press Ctrl+C in the watcher window after authentication succeeds"
    wait $WATCHER_PID
else
    echo "✅ Gmail already authenticated"
fi

echo ""
echo "Step 2: Creating test email action item..."
echo "-----------------------------------------------"
./venv/bin/python3 << 'EOF'
from pathlib import Path
from datetime import datetime

vault = Path('AI_Employee_Vault')
needs_action = vault / 'Needs_Action'

content = f"""---
type: email
source: test_script
from: test.client@example.com
subject: Project Inquiry - Need Information
received: {datetime.now().isoformat()}
priority: high
status: pending
message_id: test-{datetime.now().timestamp()}
---

## Email Content

Hi,

I'm interested in learning more about your services. Could you provide information about:
- Your pricing structure
- Timeline for typical projects
- Available consultation slots

Looking forward to hearing from you.

Best regards,
Test Client

## Suggested Actions

- [ ] Read and understand the email
- [ ] Draft a reply
- [ ] Send reply after approval
"""

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f'EMAIL_{timestamp}_test_client.md'
filepath = needs_action / filename

filepath.write_text(content, encoding='utf-8')
print(f"✅ Created: {filename}")
EOF

echo ""
echo "Step 3: Drafting email reply..."
echo "-----------------------------------------------"
./venv/bin/python3 skills/email_drafter.py

echo ""
echo "Step 4: Review the draft reply..."
echo "-----------------------------------------------"
echo "📁 Check: AI_Employee_Vault/Pending_Approval/"
ls -lh AI_Employee_Vault/Pending_Approval/EMAIL_REPLY_*.md 2>/dev/null | tail -1

echo ""
echo "✋ MANUAL STEP:"
echo "   1. Open the file in Pending_Approval/"
echo "   2. Review and edit the reply content if needed"
echo "   3. Move the file to Approved/ folder"
echo ""
read -p "Press ENTER when you've moved the file to Approved/..."

echo ""
echo "Step 5: Sending email reply..."
echo "-----------------------------------------------"
echo "📧 Email will be sent via Gmail"
echo ""
./venv/bin/python3 skills/gmail_reply_handler.py

echo ""
echo "=============================================="
echo "GMAIL WORKFLOW TEST COMPLETE"
echo "=============================================="
echo ""
echo "Check AI_Employee_Vault/Done/ for execution logs"
