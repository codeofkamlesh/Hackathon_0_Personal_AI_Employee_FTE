# AI Employee Watchers - Quick Start Guide

## 🚀 Quick Start (3 Steps)

### Step 1: Authenticate Gmail (One-Time Setup)
```bash
./venv/bin/python watchers/gmail_watcher.py
```
- Browser opens automatically
- Sign in and click "Allow"
- Press Ctrl+C after you see "Using real Gmail API"

### Step 2: Start Both Watchers
```bash
./start_watchers.sh
```

### Step 3: Check Status
```bash
./status_watchers.sh
```

---

## 📊 What Each Watcher Does

### Gmail Watcher
- **Checks:** Every 2 minutes
- **Monitors:** Unread + Important emails
- **Creates:** Action files in `AI_Employee_Vault/Needs_Action/`
- **Format:** `EMAIL_YYYYMMDD_HHMMSS_Subject.md`

### LinkedIn Watcher
- **Checks:** Every 1 hour
- **Monitors:** Time since last post (24 hours)
- **Creates:** LinkedIn post opportunities
- **Format:** `LINKEDIN_POST_YYYYMMDD_HHMMSS.md`

---

## 🎮 Control Commands

### Using Screen Sessions (Recommended)

**Start watchers:**
```bash
./start_watchers.sh
```

**Check status:**
```bash
./status_watchers.sh
```

**View live logs:**
```bash
# Gmail watcher
screen -r gmail_watcher

# LinkedIn watcher
screen -r linkedin_watcher

# Detach (keep running): Press Ctrl+A then D
```

**Stop watchers:**
```bash
./stop_watchers.sh
```

---

### Using Simple Background Processes

**Start:**
```bash
./start_watchers_simple.sh
```

**View logs:**
```bash
tail -f logs/gmail_watcher.log
tail -f logs/linkedin_watcher.log
```

**Stop:**
```bash
./stop_watchers_simple.sh
```

---

### Using Systemd Services (Production)

**Install (one-time):**
```bash
chmod +x install_services.sh
./install_services.sh
```

**Control:**
```bash
# Status
sudo systemctl status gmail-watcher
sudo systemctl status linkedin-watcher

# Stop
sudo systemctl stop gmail-watcher
sudo systemctl stop linkedin-watcher

# Start
sudo systemctl start gmail-watcher
sudo systemctl start linkedin-watcher

# View logs
sudo journalctl -u gmail-watcher -f
sudo journalctl -u linkedin-watcher -f
```

---

## 🔄 Complete Workflow

### 1. Watchers Create Action Items
```
Gmail Watcher → Detects important email
                ↓
AI_Employee_Vault/Needs_Action/EMAIL_*.md

LinkedIn Watcher → Time for post (every 24h)
                   ↓
AI_Employee_Vault/Needs_Action/LINKEDIN_POST_*.md
```

### 2. Process Action Items
```bash
# Use the reasoning-loop skill to create plans
claude /reasoning-loop

# Use the process-needs-action skill to execute
claude /process-needs-action
```

### 3. Review & Approve
```bash
# Check pending approvals
ls -la AI_Employee_Vault/Pending_Approval/

# LinkedIn posts require approval before posting
```

### 4. Monitor Results
```bash
# Check completed items
ls -la AI_Employee_Vault/Done/

# View vault status
claude /read-vault-status
```

---

## 📁 File Structure

```
AI_Employee_Vault/
├── Needs_Action/          ← Watchers create files here
│   ├── EMAIL_*.md
│   └── LINKEDIN_POST_*.md
├── Pending_Approval/      ← Items awaiting human review
│   └── LINKEDIN_POST_*.md
└── Done/                  ← Completed items
    ├── EMAIL_*.md
    └── EXECUTED_LINKEDIN_POST_*.md
```

---

## 🔍 Monitoring & Debugging

### Check if watchers are running
```bash
# Screen sessions
screen -list

# Background processes
ps aux | grep watcher

# Systemd services
sudo systemctl status gmail-watcher linkedin-watcher
```

### View recent activity
```bash
# Recent action files
ls -lt AI_Employee_Vault/Needs_Action/

# Watcher state
cat watchers/.gmail_watcher_state.json
cat watchers/.linkedin_watcher_state.json
```

### Test Gmail connection
```bash
./venv/bin/python -c "
from watchers.gmail_watcher import GmailWatcher
watcher = GmailWatcher('AI_Employee_Vault')
print('Gmail API:', 'Connected' if watcher.service else 'Failed')
"
```

---

## ⚙️ Configuration

### Gmail Watcher Settings
Edit `watchers/gmail_watcher.py`:

```python
# Line 115: Check interval (seconds)
super().__init__(vault_path, check_interval=120)  # 2 minutes

# Line 163: Email query
messages = self.service.list_messages('is:unread is:important')

# Other query examples:
# 'is:unread'                          # All unread
# 'from:client@example.com is:unread'  # Specific sender
# 'subject:urgent is:unread'           # Specific subject
```

### LinkedIn Watcher Settings
Edit `watchers/linkedin_watcher.py`:

```python
# Line 26: Check interval (seconds)
super().__init__(vault_path, check_interval=3600)  # 1 hour

# Line 34: Post frequency (hours)
self.post_frequency_hours = 24  # Once per day
```

---

## 🐛 Troubleshooting

### Gmail watcher shows "Using mock Gmail service"
**Problem:** Gmail API not authenticated or credentials missing

**Solution:**
```bash
# Check credentials exist
ls -la credentials.json

# Re-authenticate
rm token.pickle
./venv/bin/python watchers/gmail_watcher.py
```

### Import errors in IDE
**Problem:** IDE using wrong Python interpreter

**Solution:**
1. VS Code: Ctrl+Shift+P → "Python: Select Interpreter" → Choose `./venv/bin/python`
2. Or reload window: Ctrl+Shift+P → "Developer: Reload Window"

### Watchers not creating files
**Problem:** Vault directory doesn't exist or permissions issue

**Solution:**
```bash
# Check vault exists
ls -la AI_Employee_Vault/Needs_Action/

# Create if missing
mkdir -p AI_Employee_Vault/Needs_Action

# Check permissions
chmod -R u+w AI_Employee_Vault/
```

### Screen session not found
**Problem:** Screen not installed

**Solution:**
```bash
# Install screen
sudo apt-get install screen

# Or use simple background processes instead
./start_watchers_simple.sh
```

---

## 🎯 Next Steps

1. **Start watchers:** `./start_watchers.sh`
2. **Test Gmail:** Send yourself an important email
3. **Wait 2 minutes:** Check `AI_Employee_Vault/Needs_Action/`
4. **Process items:** `claude /process-needs-action`
5. **Approve posts:** Review `AI_Employee_Vault/Pending_Approval/`

---

## 📚 Additional Resources

- Gmail Setup: `GMAIL_SETUP.md`
- Project Status: `STATUS.md`
- Completion Report: `COMPLETION_REPORT.md`

---

## 💡 Tips

- **Gmail:** Mark emails as "Important" (⭐) to trigger watcher
- **LinkedIn:** Watcher creates opportunities, Claude drafts content
- **Approval:** LinkedIn posts ALWAYS require human approval
- **Logs:** Check logs if something isn't working
- **State:** Watchers remember what they've processed (`.json` files)

---

## 🆘 Getting Help

If issues persist:
1. Check logs: `tail -f logs/*.log`
2. Verify Python environment: `./venv/bin/python --version`
3. Test imports: `./venv/bin/python -c "import google.auth; print('OK')"`
4. Review watcher state files in `watchers/`
