# Bronze Tier Demo - Complete Walkthrough

This guide demonstrates the complete Bronze tier AI Employee system in action.

## System Overview

The Bronze tier provides:
- **Perception**: File System Watcher monitors the Inbox folder
- **Memory**: Obsidian vault stores all data locally
- **Reasoning**: Claude Code processes tasks using Agent Skills
- **Action**: Files are processed and moved through the workflow

## Demo Walkthrough

### Step 1: Check Initial System Status

```bash
python3 skills/read_vault_status.py
```

**Expected Output:**
- All folders exist and are empty (or have minimal items)
- Dashboard shows no activity
- No pending actions

### Step 2: Start the File System Watcher

Open a terminal and run:

```bash
cd watchers
python3 filesystem_watcher.py ../AI_Employee_Vault ../AI_Employee_Vault/Inbox
```

**What happens:**
- Watcher starts monitoring the Inbox folder
- Checks every 30 seconds for new files
- Logs activity to console

**Console output:**
```
2026-02-20 01:14:25 - FileSystemWatcher - INFO - Starting FileSystemWatcher
2026-02-20 01:14:25 - FileSystemWatcher - INFO - Monitoring vault at: ../AI_Employee_Vault
2026-02-20 01:14:25 - FileSystemWatcher - INFO - Check interval: 30 seconds
```

### Step 3: Drop a Test File

In another terminal, create a test file:

```bash
echo "Important client document for review" > AI_Employee_Vault/Inbox/client_proposal.txt
```

**What happens:**
- Watcher detects the new file within 30 seconds
- Creates an action file in Needs_Action folder
- Logs the detection

**Watcher console output:**
```
2026-02-20 01:14:25 - FileSystemWatcher - INFO - Found 1 new item(s) to process
2026-02-20 01:14:25 - FileSystemWatcher - INFO - Created action file: FILE_20260220_011425_client_proposal.md
```

### Step 4: Review the Action File

Check what the watcher created:

```bash
cat AI_Employee_Vault/Needs_Action/FILE_*_client_proposal.md
```

**Content includes:**
- File metadata (name, size, type, location)
- Detection timestamp
- Status: pending
- Priority: medium
- Suggested actions checklist
- Space for processing notes

### Step 5: Check Updated Vault Status

```bash
python3 skills/read_vault_status.py
```

**Expected Output:**
```
FOLDER STATUS:
  Inbox                ✓ (1 items)
  Needs_Action         ✓ (1 items)
  Done                 ✓ (0 items)

PENDING ACTIONS:
  • FILE_20260220_011425_client_proposal.md
```

### Step 6: Process with Claude Code

Start Claude Code:

```bash
claude
```

Then interact with Claude:

**You:** "Show me the vault status"

**Claude:** [Uses read_vault_status skill and displays current state]

**You:** "Process all files in Needs_Action"

**Claude:** [Uses process_needs_action skill to process the file]

### Step 7: Verify Processing Results

```bash
python3 skills/read_vault_status.py
```

**Expected Output:**
```
FOLDER STATUS:
  Inbox                ✓ (1 items)
  Needs_Action         ✓ (0 items)
  Done                 ✓ (1 items)

DASHBOARD SUMMARY:
  - [2026-02-20 01:16] Processed 1 file(s) from Needs_Action

✓ No pending actions
```

### Step 8: Review Completed Task

Check the Done folder:

```bash
ls -la AI_Employee_Vault/Done/
cat AI_Employee_Vault/Done/20260220_*_client_proposal.md
```

**What you'll see:**
- Original action file content
- Processing timestamp added at the bottom
- File renamed with timestamp prefix

### Step 9: Check Dashboard

```bash
cat AI_Employee_Vault/Dashboard.md
```

**Dashboard shows:**
- System status: Active
- Recent activity: "Processed 1 file(s) from Needs_Action"
- Updated timestamp

## Complete Workflow Diagram

```
1. User drops file
   └─> AI_Employee_Vault/Inbox/client_proposal.txt

2. Watcher detects (within 30 seconds)
   └─> Creates: Needs_Action/FILE_*_client_proposal.md

3. Claude Code reads Needs_Action
   └─> Processes according to Company_Handbook.md rules

4. File moves to Done
   └─> Done/20260220_*_FILE_*_client_proposal.md

5. Dashboard updates
   └─> Logs activity with timestamp
```

## Testing Different File Types

Try dropping different files to see how the system handles them:

```bash
# Text document
echo "Meeting notes" > AI_Employee_Vault/Inbox/notes.txt

# CSV data
echo "name,email\nJohn,john@example.com" > AI_Employee_Vault/Inbox/contacts.csv

# JSON data
echo '{"task": "Review proposal", "priority": "high"}' > AI_Employee_Vault/Inbox/task.json

# Image (if you have one)
cp ~/Pictures/screenshot.png AI_Employee_Vault/Inbox/
```

Each file will be detected, cataloged, and processed according to the workflow.

## Customization Examples

### Change Watcher Polling Interval

Edit `watchers/filesystem_watcher.py`:

```python
# Change from 30 seconds to 10 seconds
watcher = FileSystemWatcher(
    vault_path=vault_path,
    drop_folder=drop_folder,
    check_interval=10  # Changed from 30
)
```

### Add Custom Processing Rules

Edit `AI_Employee_Vault/Company_Handbook.md`:

```markdown
## File Processing Rules

### By File Type
- **.txt files**: Review and summarize
- **.csv files**: Import to database
- **.pdf files**: Extract text and index
- **.json files**: Parse and validate
```

### Create Custom Action Priority

Edit the watcher to set priority based on filename:

```python
priority = "high" if "urgent" in file_path.name.lower() else "medium"
```

## Troubleshooting

### Watcher Not Detecting Files

**Problem:** Files dropped in Inbox aren't being detected

**Solutions:**
1. Check watcher is running: `ps aux | grep filesystem_watcher`
2. Verify Inbox path is correct
3. Check file permissions
4. Look for errors in watcher console output

### Files Not Moving to Done

**Problem:** process_needs_action runs but files stay in Needs_Action

**Solutions:**
1. Check file permissions on Done folder
2. Verify no errors in console output
3. Ensure files are valid markdown (.md extension)

### Dashboard Not Updating

**Problem:** Dashboard.md doesn't show recent activity

**Solutions:**
1. Check Dashboard.md file permissions
2. Verify the file exists and is readable
3. Look for errors in process_needs_action output

## Next Steps

Once you're comfortable with Bronze tier:

1. **Add more watchers**: Gmail, WhatsApp, LinkedIn
2. **Implement MCP servers**: For external actions (email, social media)
3. **Add approval workflow**: Human-in-the-loop for sensitive actions
4. **Schedule operations**: Use cron for daily briefings
5. **Upgrade to Silver tier**: See main documentation

## Success Criteria

Your Bronze tier is complete when:

- ✓ Watcher runs continuously without errors
- ✓ Files dropped in Inbox are detected within 30 seconds
- ✓ Action files are created in Needs_Action with proper metadata
- ✓ Claude Code can read and process action files
- ✓ Processed files move to Done with timestamps
- ✓ Dashboard updates with activity logs
- ✓ All folders exist and are properly structured

## Congratulations!

You've successfully built a Bronze tier Personal AI Employee. This foundation provides:

- Local-first data storage
- Automated file monitoring
- Task queue management
- Activity logging
- Extensible skill system

You're now ready to expand to Silver tier with email monitoring, external actions, and human-in-the-loop approvals.
