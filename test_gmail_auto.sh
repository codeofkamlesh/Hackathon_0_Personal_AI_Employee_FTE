#!/bin/bash
# Updated Gmail Auto Test - Uses browser automation like LinkedIn

echo "=============================================="
echo "AUTOMATED GMAIL TEST (Browser Automation)"
echo "=============================================="
echo ""

cd "/mnt/c/Users/Admin/Documents/GitHub/Hackathon_0_Personal_AI_Employee_FTE"

# Check if Playwright is installed
echo "Checking Playwright installation..."
if ! python3 -c "import playwright" 2>/dev/null; then
    echo "❌ Playwright not installed"
    echo "Installing Playwright..."
    pip install playwright
    playwright install chromium
fi

# Check if Chromium is installed
if ! playwright --version 2>/dev/null; then
    echo "Installing Playwright browsers..."
    playwright install chromium
fi

echo "✅ Playwright ready"
echo ""

# Clean up old test emails from Approved folder
echo "Cleaning up old test files..."
python3 << 'EOF'
from pathlib import Path

vault = Path('AI_Employee_Vault')
approved = vault / 'Approved'

# Remove old test emails
for old_file in approved.glob('EMAIL_REPLY_*_test.md'):
    old_file.unlink()
    print(f"  Removed: {old_file.name}")

print("✅ Approved folder cleaned")
EOF

echo ""

# Create test email in Approved folder
echo "Creating test email in Approved folder..."
python3 << 'EOF'
from pathlib import Path
from datetime import datetime

vault = Path('AI_Employee_Vault')
approved = vault / 'Approved'
approved.mkdir(exist_ok=True)

content = f"""---
type: email_reply
to: test@example.com
subject: Re: Test Email - AI Employee
created: {datetime.now().isoformat()}
status: approved
---

# Email Reply

## Draft Reply

Thank you for your email.

This is an automated test reply from the AI Employee system to verify Gmail automation is working correctly.

Best regards,
AI Employee System
"""

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filepath = approved / f'EMAIL_REPLY_{timestamp}_test.md'
filepath.write_text(content, encoding='utf-8')
print(f"✅ Created: {filepath.name}")
EOF

echo ""
echo "=============================================="
echo "STARTING AUTOMATED EMAIL SENDING"
echo "=============================================="
echo ""
echo "📌 What will happen:"
echo "   1. Chromium browser will open"
echo "   2. Gmail will load"
echo "   3. Sign in if needed (saved for next time)"
echo "   4. Press ENTER after you see your inbox"
echo "   5. Email will auto-compose"
echo "   6. Type 'SEND' to send"
echo "   7. Browser stays open for verification"
echo ""
echo "Press ENTER to start..."
read

# Run the handler ONCE (not in a loop)
python3 skills/automated_gmail_handler.py

echo ""
echo "=============================================="
echo "TEST COMPLETE"
echo "=============================================="
echo ""
echo "Check AI_Employee_Vault/Done/ for execution log"
echo ""
echo "To test again, run: ./test_gmail_auto.sh"
