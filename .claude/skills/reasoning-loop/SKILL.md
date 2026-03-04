---
name: reasoning-loop
description: |
  Generate structured Plan.md files for action items in the Needs_Action folder.
  Analyzes pending tasks and creates detailed execution plans with step-by-step strategies.
---

# Reasoning Loop

Automatically generate execution plans for tasks in the Needs_Action queue.

## What It Does

1. Scans `/Needs_Action` folder for pending action items
2. Parses each action file and extracts metadata
3. Analyzes the action type and context
4. Generates structured Plan.md files in `/Plans` folder with:
   - Objective and context
   - Step-by-step action items
   - Decision points and branching logic
   - Approval requirements
   - Next actions

## When to Use

- After watchers create new action items
- Before processing tasks in Needs_Action
- As part of automated workflow
- When you need structured plans for complex tasks

## Usage

Simply invoke this skill and it will process all pending actions:

```
/reasoning-loop
```

Or ask naturally:
```
Generate plans for all items in Needs_Action
Create execution plans for pending tasks
```

## Plan Types Generated

- **Email Plans**: Response strategy, urgency analysis
- **LinkedIn Post Plans**: Content guidelines, approval workflow
- **File Processing Plans**: Type detection, processing steps
- **Generic Plans**: Flexible for any action type

## Output

Plans are created as Markdown files in `/Plans` folder with format:
```
PLAN_[timestamp]_[original_filename].md
```

## Integration

- **Input**: `/Needs_Action/*.md` files
- **Output**: `/Plans/PLAN_*.md` files
- **References**: `Company_Handbook.md` for guidelines
