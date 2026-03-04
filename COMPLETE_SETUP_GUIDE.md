# AI Employee - Complete Setup & Usage Guide

## 🎯 What This System Does

**Gmail Automation:**
- Monitors your Gmail for important/unread emails
- Drafts professional replies
- Requires your approval before sending
- Opens browser for Gmail authentication

**LinkedIn Automation:**
- Creates LinkedIn posting opportunities (every 24 hours)
- Drafts professional business posts
- Requires your approval before posting
- Opens browser for LinkedIn authentication and posting

**Human-in-the-Loop (HITL):**
- ALL actions require your explicit approval
- You can edit drafts before approving
- Browser opens for authentication when needed
- Complete audit trail of all actions

---

## 📦 Installation (One-Time Setup)

### Step 1: Run Complete Installation
```bash
chmod +x install_complete.sh
./install_complete.sh
```

This installs:
- Python dependencies (Gmail API, etc.)
- Playwright (browser automation)
- Email MCP server
- All required tools

### Step 2: Authenticate Gmail (One-Time)
```bash
./venv/bin/python3 watchers/gmail_watcher.py
```

**What happens:**
- Browser opens automatically
- Sign in to your Google account
- Click "Allow" for Gmail permissions
- Token saved (you won't need to do this again)
- Press **Ctrl+C** after you see "Using real Gmail API"

---

## 🧪 Testing Individual Workflows

### Test LinkedIn Workflow (Separate)
```bash
./test_linkedin_workflow.sh
```

**What happens:**
1. Creates a LinkedIn posting opportunity
2. Drafts a professional post
3. Saves to `Pending_Approval/` folder
4. **YOU REVIEW** and move to `Approved/`
5. Browser opens for LinkedIn sign-in
6. **YOU APPROVE** final posting
7. Post published to your LinkedIn
8. Execution log saved to `Done/`

**Timeline:** ~5 minutes (includes your review time)

---

### Test Gmail Workflow (Separate)
```bash
./test_gmail_workflow.sh
```

**What happens:**
1. Creates a test email action item
2. Drafts a professional reply
3. Saves to `Pending_Approval/` folder
4. **YOU REVIEW** and move to `Approved/`
5. Email sent via Gmail (mock mode by default)
6. Execution log saved to `Done/`

**Timeline:** ~3 minutes (includes your review time)

---

## 🚀 Running Both Together (Production Mode)

### Option 1: Manual Control (Recommended for Testing)

**Terminal 1 - Start Watchers:**
```bash
./start_watchers.sh
```
This starts:
- Gmail watcher (checks every 2 minutes)
- LinkedIn watcher (checks every 1 hour)

**Terminal 2 - Start Orchestrator:**
```bash
./orchestrator.sh
```
This monitors:
- `Needs_Action/` folder (processes new items)
- `Approved/` folder (executes approved actions)

**Check Status:**
```bash
./status_watchers.sh
```

**Stop Everything:**
```bash
./stop_watchers.sh
# Press Ctrl+C in orchestrator terminal
```

---

### Option 2: Fully Automated (Background)

**Start everything in background:**
```bash
# Start watchers
./start_watchers.sh

# Start orchestrator in background
nohup ./orchestrator.sh > logs/orchestrator.log 2>&1 &
echo $! > .orchestrator.pid
```

**Check logs:**
```bash
tail -f logs/orchestrator.log
tail -f logs/gmail_watcher.log
tail -f logs/linkedin_watcher.log
```

**Stop everything:**
```bash
./stop_watchers.sh
kill $(cat .orchestrator.pid)
rm .orchestrator.pid
```

---

## 📋 Complete Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    GMAIL WORKFLOW                            │
└─────────────────────────────────────────────────────────────┘

Gmail Inbox (Important Email)
        ↓
Gmail Watcher (every 2 min)
        ↓
Creates: Needs_Action/EMAIL_*.md
        ↓
Email Drafter (orchestrator)
        ↓
Creates: Pending_Approval/EMAIL_REPLY_*.md
        ↓
[YOU REVIEW & EDIT]
        ↓
Move to: Approved/EMAIL_REPLY_*.md
        ↓
Gmail Reply Handler (orchestrator)
        ↓
Browser opens → Gmail sign-in → Send email
        ↓
Creates: Done/SENT_EMAIL_REPLY_*.md


┌─────────────────────────────────────────────────────────────┐
│                  LINKEDIN WORKFLOW                           │
└─────────────────────────────────────────────────────────────┘

LinkedIn Watcher (every 24 hours)
        ↓
Creates: Needs_Action/LINKEDIN_POST_*.md
        ↓
LinkedIn Drafter (orchestrator)
        ↓
Creates: Pending_Approval/LINKEDIN_POST_*.md
        ↓
[YOU REVIEW & EDIT]
        ↓
Move to: Approved/LINKEDIN_POST_*.md
        ↓
LinkedIn Poster (orchestrator)
        ↓
Browser opens → LinkedIn sign-in → Post content
        ↓
Creates: Done/EXECUTED_LINKEDIN_POST_*.md
```

---

## 🎮 Step-by-Step Commands

### For Testing LinkedIn ONLY:
```bash
# 1. Install (one-time)
./install_complete.sh

# 2. Test LinkedIn workflow
./test_linkedin_workflow.sh

# Follow prompts:
# - Review draft in Pending_Approval/
# - Move to Approved/
# - Sign in to LinkedIn when browser opens
# - Approve final posting
```

### For Testing Gmail ONLY:
```bash
# 1. Install (one-time)
./install_complete.sh

# 2. Authenticate Gmail (one-time)
./venv/bin/python3 watchers/gmail_watcher.py
# Press Ctrl+C after authentication

# 3. Test Gmail workflow
./test_gmail_workflow.sh

# Follow prompts:
# - Review draft in Pending_Approval/
# - Move to Approved/
# - Confirm sending
```

### For Running BOTH Together:
```bash
# 1. Install (one-time)
./install_complete.sh

# 2. Authenticate Gmail (one-time)
./venv/bin/python3 watchers/gmail_watcher.py
# Press Ctrl+C after authentication

# 3. Start watchers (Terminal 1)
./start_watchers.sh

# 4. Start orchestrator (Terminal 2)
./orchestrator.sh

# 5. Check status anytime (Terminal 3)
./status_watchers.sh

# 6. Stop everything
./stop_watchers.sh
# Press Ctrl+C in orchestrator terminal
```

---

## 📁 Folder Structure & What Goes Where

```
AI_Employee_Vault/
├── Needs_Action/          ← Watchers create files here
│   ├── EMAIL_*.md         (from Gmail watcher)
│   └── LINKEDIN_POST_*.md (from LinkedIn watcher)
│
├── Pending_Approval/      ← Drafts waiting for YOUR review
│   ├── EMAIL_REPLY_*.md   (email drafts)
│   └── LINKEDIN_POST_*.md (LinkedIn drafts)
│
├── Approved/              ← YOU move files here to approve
│   ├── EMAIL_REPLY_*.md   (ready to send)
│   └── LINKEDIN_POST_*.md (ready to post)
│
├── Rejected/              ← YOU move files here to reject
│
└── Done/                  ← Completed actions with logs
    ├── SENT_EMAIL_*.md
    └── EXECUTED_LINKEDIN_POST_*.md
```

---

## 🔐 Authentication & Security

### Gmail Authentication:
- **Method:** OAuth 2.0 (official Google method)
- **Token:** Saved to `token.pickle` (never commit to git)
- **Permissions:** Read emails + Send emails
- **Browser:** Opens automatically for sign-in
- **Frequency:** One-time (token auto-refreshes)

### LinkedIn Authentication:
- **Method:** Browser automation (Playwright)
- **Session:** You sign in each time (for security)
- **Permissions:** Post to your feed
- **Browser:** Opens for each posting session
- **Frequency:** Per posting session

### Security Features:
- ✅ All credentials stored locally
- ✅ No credentials in code
- ✅ Human approval required for all actions
- ✅ Complete audit trail
- ✅ Edit drafts before approving
- ✅ Easy rejection option

---

## 🐛 Troubleshooting

### Gmail watcher shows "Using mock Gmail service"
**Problem:** Not authenticated or credentials missing

**Solution:**
```bash
# Check credentials exist
ls -la credentials.json

# Re-authenticate
rm token.pickle
./venv/bin/python3 watchers/gmail_watcher.py
```

### LinkedIn posting fails
**Problem:** Browser automation issue

**Solution:**
```bash
# Reinstall Playwright
./venv/bin/pip install --upgrade playwright
./venv/bin/playwright install chromium

# Test browser
./venv/bin/playwright open https://linkedin.com
```

### Orchestrator not processing files
**Problem:** Files not in correct folder

**Solution:**
```bash
# Check folder structure
ls -la AI_Employee_Vault/*/

# Ensure files are in Approved/ folder
mv AI_Employee_Vault/Pending_Approval/LINKEDIN_POST_*.md AI_Employee_Vault/Approved/
```

### Import errors in Python
**Problem:** Virtual environment not activated

**Solution:**
```bash
# Always use venv Python
./venv/bin/python3 script.py

# NOT just: python3 script.py
```

---

## 📊 Monitoring & Logs

### Check watcher status:
```bash
./status_watchers.sh
```

### View live logs:
```bash
# Gmail watcher
screen -r gmail_watcher

# LinkedIn watcher
screen -r linkedin_watcher

# Orchestrator
tail -f logs/orchestrator.log
```

### Check recent activity:
```bash
# Recent action items
ls -lt AI_Employee_Vault/Needs_Action/

# Pending approvals
ls -lt AI_Employee_Vault/Pending_Approval/

# Completed items
ls -lt AI_Employee_Vault/Done/
```

---

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| Install everything | `./install_complete.sh` |
| Authenticate Gmail | `./venv/bin/python3 watchers/gmail_watcher.py` |
| Test LinkedIn only | `./test_linkedin_workflow.sh` |
| Test Gmail only | `./test_gmail_workflow.sh` |
| Start watchers | `./start_watchers.sh` |
| Start orchestrator | `./orchestrator.sh` |
| Check status | `./status_watchers.sh` |
| Stop watchers | `./stop_watchers.sh` |
| View logs | `tail -f logs/*.log` |

---

## ✅ Success Checklist

Before running in production, verify:

- [ ] `./install_complete.sh` completed successfully
- [ ] Gmail authenticated (token.pickle exists)
- [ ] LinkedIn test workflow works
- [ ] Gmail test workflow works
- [ ] Watchers start without errors
- [ ] Orchestrator processes files correctly
- [ ] Browser opens for authentication
- [ ] Approval workflow works (move files between folders)
- [ ] Execution logs appear in Done/

---

## 🆘 Getting Help

If you encounter issues:

1. **Check logs:** `tail -f logs/*.log`
2. **Verify installation:** `./install_complete.sh`
3. **Test individually:** Run test scripts first
4. **Check folder structure:** Ensure files are in correct folders
5. **Re-authenticate:** Delete token.pickle and re-auth

---

## 📚 Additional Documentation

- `WATCHER_GUIDE.md` - Detailed watcher documentation
- `GMAIL_SETUP.md` - Gmail API setup guide
- `STATUS.md` - Project status and features
- `COMPLETION_REPORT.md` - Implementation details

---

**Ready to start? Run:** `./install_complete.sh`
