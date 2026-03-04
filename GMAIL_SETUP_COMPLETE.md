# Gmail Automation - Complete Setup Guide

## What Changed

✅ **OLD (Broken):** Browser automation with Playwright - unreliable, slow, requires manual clicking
✅ **NEW (Working):** Gmail API - fast, reliable, fully automated

## Quick Setup (2 Minutes)

### Option 1: Automated Setup Script

```bash
cd /mnt/c/Users/Admin/Documents/GitHub/Hackathon_0_Personal_AI_Employee_FTE
./setup_gmail_send.sh
```

Follow the prompts to authenticate.

### Option 2: Manual Setup

```bash
cd /mnt/c/Users/Admin/Documents/GitHub/Hackathon_0_Personal_AI_Employee_FTE
python3 authenticate_gmail_send.py
```

**Steps:**
1. Script will display a URL
2. Copy the URL and open in your Windows browser
3. Sign in to Gmail
4. Click "Allow" to grant send permission
5. Copy the authorization code from the URL
6. Paste it back in the terminal
7. Done! ✅

## Testing

After authentication, test the system:

```bash
./test_gmail_auto.sh
```

This will:
1. Create a test email in `Approved` folder
2. Automatically send it via Gmail API
3. Move it to `Done` folder with execution log

## How It Works Now

### Architecture (Following Hackathon Requirements)

```
Approved Folder
    ↓
automated_gmail_handler.py
    ↓
Gmail API (OAuth 2.0)
    ↓
Email Sent ✅
    ↓
Execution Log → Done Folder
```

### Key Features

✅ **No Browser Needed** - Direct API calls
✅ **Fully Automated** - Compose and send automatically
✅ **HITL Approval** - Emails must be in Approved folder first
✅ **Secure** - OAuth 2.0 authentication
✅ **Fast** - Sends in seconds
✅ **Reliable** - No UI changes breaking automation

## What You Can Do Now

### 1. Send Test Email

```bash
./test_gmail_auto.sh
```

### 2. Create Your Own Email

Create a file in `AI_Employee_Vault/Approved/` with this format:

```markdown
---
type: email_reply
to: recipient@example.com
subject: Your Subject Here
created: 2026-03-04T12:00:00
status: approved
---

# Email Reply

## Draft Reply

Your email content here.

This will be sent automatically.

Best regards,
Your Name
```

Then run:
```bash
python3 skills/automated_gmail_handler.py
```

### 3. Integrate with Workflow

The Gmail watcher will:
1. Detect important emails → Create action in `Needs_Action`
2. Reasoning loop → Generate plan in `Plans`
3. You draft reply → Move to `Pending_Approval`
4. You approve → Move to `Approved`
5. **Automated handler → Send via Gmail API** ✅
6. Execution log → `Done` folder

## Troubleshooting

### "OAuth client was disabled"
- Your old token doesn't have send permission
- Run: `rm token_send.pickle && python3 authenticate_gmail_send.py`

### "credentials.json not found"
- Make sure it's in the project root
- Download from Google Cloud Console

### "Invalid grant"
- Token expired
- Run: `python3 authenticate_gmail_send.py`

### "Permission denied"
- Make sure you granted "Send email on your behalf" permission
- Re-authenticate and click "Allow"

## Silver Tier Status

With this update, your Silver Tier Gmail automation is **COMPLETE**:

✅ Gmail watcher (monitors inbox)
✅ Email action creation
✅ Plan generation
✅ HITL approval workflow
✅ **Automatic email sending via Gmail API** ← NEW!
✅ Execution logging

## Next: Gold Tier

Once Gmail automation is working, you can move to Gold Tier features:
- Ralph Wiggum loop (autonomous iteration)
- Monday Morning CEO Briefing
- Cross-domain integration
- Accounting system (Odoo)
- Weekly business audit

---

**Ready to test?** Run: `./setup_gmail_send.sh`
