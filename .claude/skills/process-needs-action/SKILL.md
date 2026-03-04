---
name: process-needs-action
description: |
  Process tasks from the Needs_Action queue. Reads action items, executes them
  according to their plans, and moves completed items to Done folder.
---

# Process Needs Action

Execute tasks from the Needs_Action queue.

## What It Does

1. Reads tasks from `/Needs_Action` folder
2. Checks for corresponding plans in `/Plans` folder
3. Executes tasks according to plan steps
4. Moves completed items to `/Done` folder
5. Logs all actions taken

## When to Use

- After plans have been generated
- To execute pending tasks
- As part of automated workflow
- During manual task processing sessions

## Usage

```
/process-needs-action
```

Or ask naturally:
```
Process the pending tasks
Execute items in Needs_Action
Work on the task queue
```

## Task Types Handled

- **Email Tasks**: Draft responses, forward, archive
- **File Processing**: Analyze, categorize, extract info
- **LinkedIn Posts**: Prepare for approval workflow
- **Generic Tasks**: Follow plan instructions

## Workflow

```
Needs_Action → Check Plan → Execute → Done
                    ↓
              (if needs approval)
                    ↓
            Pending_Approval
```

## Safety

- Respects approval requirements
- Never executes sensitive actions without HITL
- Logs all operations
- Handles errors gracefully

## Output

- Completed tasks moved to `/Done`
- Execution logs created
- Dashboard updated
- Status summary displayed
