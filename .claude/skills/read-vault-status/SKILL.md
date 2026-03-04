---
name: read-vault-status
description: |
  Display current status of the AI Employee Vault including pending tasks,
  completed items, and approval requests. Provides a quick overview of system state.
---

# Read Vault Status

Get a comprehensive overview of the AI Employee Vault state.

## What It Does

Scans all vault folders and provides counts and summaries:
- Inbox items waiting to be processed
- Needs_Action tasks pending
- Plans generated
- Pending approvals requiring review
- Approved items ready for execution
- Completed tasks in Done folder
- Rejected items

## When to Use

- Check system status at a glance
- Before processing tasks
- After running watchers
- During daily reviews
- Troubleshooting workflow issues

## Usage

```
/read-vault-status
```

Or ask naturally:
```
What's the current vault status?
Show me pending tasks
How many items need approval?
```

## Output Format

Displays organized summary:
```
AI Employee Vault Status
========================

Inbox: 3 files
Needs_Action: 5 tasks
Plans: 5 plans
Pending_Approval: 2 items
Approved: 1 item
Done: 15 completed
Rejected: 0 items

Recent Activity:
- [timestamp] New file in Inbox
- [timestamp] Plan generated
```

## Integration

Works with all vault folders to provide real-time status.
