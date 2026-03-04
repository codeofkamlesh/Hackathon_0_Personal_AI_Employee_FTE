#!/bin/bash
# Simple Gmail Test - Opens REAL browser window

echo "=============================================="
echo "GMAIL TEST - Real Browser Window"
echo "=============================================="
echo ""

PROJECT_DIR="/mnt/c/Users/Admin/Documents/GitHub/Hackathon_0_Personal_AI_Employee_FTE"
cd "$PROJECT_DIR"

# Step 1: Create test email reply in Approved folder
echo "Step 1: Creating test email reply..."
echo "-----------------------------------------------"
./venv/bin/python3 << 'EOF'
from pathlib import Path
from datetime import datetime

vault = Path('AI_Employee_Vault')
approved = vault / 'Approved'

content = f"""---
type: email_reply
to: test@example.com
subject: Re: Test Email
created: {datetime.now().isoformat()}
status: approved
---

# Email Reply Draft

## Original Email
- **From:** test@example.com
- **Subject:** Test Email

## Draft Reply

Thank you for your email.

This is a test reply from the AI Employee system to verify Gmail automation is working correctly.

Best regards
"""

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f'EMAIL_REPLY_{timestamp}_test.md'
filepath = approved / filename

filepath.write_text(content, encoding='utf-8')
print(f"✅ Created: {filename}")
print(f"📁 Location: {filepath}")
EOF

echo ""
echo "Step 2: Opening browser for Gmail..."
echo "-----------------------------------------------"
echo "🌐 Browser will open in 3 seconds..."
sleep 3

./venv/bin/python3 skills/simple_gmail_handler.py

echo ""
echo "=============================================="
echo "TEST COMPLETE"
echo "=============================================="
echo ""
echo "Check AI_Employee_Vault/Done/ for execution log"
