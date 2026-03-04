# AI Employee - Quick Start Commands

## 🚀 ONE-TIME SETUP (Do This First)

```bash
# 1. Install everything
./install_complete.sh

# 2. Authenticate Gmail (browser opens, sign in, press Ctrl+C after success)
./venv/bin/python3 watchers/gmail_watcher.py
```

---

## 📱 LINKEDIN ONLY (Separate Testing)

### Step-by-Step Commands:

```bash
# Run the complete LinkedIn workflow test
./test_linkedin_workflow.sh
```

**What happens:**
1. Script creates a LinkedIn posting opportunity
2. Drafts a professional post → saves to `Pending_Approval/`
3. **YOU:** Review the file, edit if needed, move to `Approved/`
4. **YOU:** Press ENTER in terminal
5. Browser opens → Sign in to LinkedIn
6. **YOU:** Review post in browser, type 'POST' to publish
7. Post goes live on your LinkedIn feed
8. Execution log saved to `Done/`

**Manual alternative (step-by-step):**
```bash
# 1. Start LinkedIn watcher
./venv/bin/python3 watchers/linkedin_watcher.py &

# 2. Wait for it to create opportunity file (or create manually)
# Check: ls AI_Employee_Vault/Needs_Action/LINKEDIN_POST_*.md

# 3. Draft the post
./venv/bin/python3 skills/linkedin_drafter.py

# 4. Review and approve
# Move file from Pending_Approval/ to Approved/

# 5. Post to LinkedIn
./venv/bin/python3 skills/linkedin_poster.py
```

---

## 📧 GMAIL ONLY (Separate Testing)

### Step-by-Step Commands:

```bash
# Run the complete Gmail workflow test
./test_gmail_workflow.sh
```

**What happens:**
1. Script creates a test email action item
2. Drafts a professional reply → saves to `Pending_Approval/`
3. **YOU:** Review the file, edit if needed, move to `Approved/`
4. **YOU:** Press ENTER in terminal
5. Email sent (mock mode by default)
6. Execution log saved to `Done/`

**Manual alternative (step-by-step):**
```bash
# 1. Start Gmail watcher
./venv/bin/python3 watchers/gmail_watcher.py &

# 2. Send yourself an important email, wait 2 minutes
# Check: ls AI_Employee_Vault/Needs_Action/EMAIL_*.md

# 3. Draft reply
./venv/bin/python3 skills/email_drafter.py

# 4. Review and approve
# Move file from Pending_Approval/ to Approved/

# 5. Send reply
./venv/bin/python3 skills/gmail_reply_handler.py
```

---

## 🔄 BOTH TOGETHER (Production Mode)

### Option A: Two Terminals (Recommended)

**Terminal 1 - Watchers:**
```bash
./start_watchers.sh
```
This runs:
- Gmail watcher (checks every 2 min)
- LinkedIn watcher (checks every 1 hour)

**Terminal 2 - Orchestrator:**
```bash
./orchestrator.sh
```
This monitors and processes:
- New items in `Needs_Action/`
- Approved items in `Approved/`

**Terminal 3 - Check Status:**
```bash
./status_watchers.sh
```

**To Stop:**
```bash
./stop_watchers.sh
# Press Ctrl+C in orchestrator terminal
```

---

### Option B: Fully Automated Background

```bash
# Start everything in background
./start_watchers.sh
nohup ./orchestrator.sh > logs/orchestrator.log 2>&1 &
echo $! > .orchestrator.pid

# Check status
./status_watchers.sh
tail -f logs/orchestrator.log

# Stop everything
./stop_watchers.sh
kill $(cat .orchestrator.pid)
rm .orchestrator.pid
```

---

## 📋 Workflow Summary

### LinkedIn Workflow:
```
Watcher → Needs_Action/ → Drafter → Pending_Approval/
→ [YOU APPROVE] → Approved/ → Poster → Browser → LinkedIn → Done/
```

### Gmail Workflow:
```
Watcher → Needs_Action/ → Drafter → Pending_Approval/
→ [YOU APPROVE] → Approved/ → Reply Handler → Gmail → Done/
```

---

## 🎯 Most Common Commands

```bash
# Install (once)
./install_complete.sh

# Authenticate Gmail (once)
./venv/bin/python3 watchers/gmail_watcher.py

# Test LinkedIn
./test_linkedin_workflow.sh

# Test Gmail
./test_gmail_workflow.sh

# Run both (Terminal 1)
./start_watchers.sh

# Run both (Terminal 2)
./orchestrator.sh

# Check status
./status_watchers.sh

# Stop
./stop_watchers.sh
```

---

## ✅ Verification Checklist

After installation, verify:

```bash
# 1. Virtual environment exists
ls -la venv/

# 2. Gmail authenticated
ls -la token.pickle

# 3. Vault structure exists
ls -la AI_Employee_Vault/

# 4. Scripts are executable
ls -la *.sh

# 5. Python dependencies installed
./venv/bin/pip list | grep google-auth

# 6. Playwright installed
./venv/bin/playwright --version
```

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Import errors | Use `./venv/bin/python3` not `python3` |
| Gmail not working | Re-run: `./venv/bin/python3 watchers/gmail_watcher.py` |
| LinkedIn fails | Reinstall: `./venv/bin/playwright install chromium` |
| Files not processing | Check they're in `Approved/` folder |
| Watchers not running | Run: `./start_watchers.sh` |

---

## 📞 Support

- Full guide: `COMPLETE_SETUP_GUIDE.md`
- Watcher details: `WATCHER_GUIDE.md`
- Gmail setup: `GMAIL_SETUP.md`
- Check logs: `tail -f logs/*.log`
