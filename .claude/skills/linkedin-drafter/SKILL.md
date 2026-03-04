---
name: linkedin-drafter
description: |
  Draft professional LinkedIn posts with Human-in-the-Loop (HITL) approval workflow.
  Creates business-focused content designed to generate sales leads. Posts NEVER published
  without explicit human approval.
---

# LinkedIn Drafter

Create professional LinkedIn posts with mandatory human approval.

## What It Does

1. Reads Company_Handbook.md for brand voice and guidelines
2. Drafts professional LinkedIn post content
3. Creates approval request in `/Pending_Approval` folder
4. Waits for human to review and approve
5. Executes approved posts (moves to Done with execution log)

## HITL Workflow

```
Draft → Pending_Approval → [Human Review] → Approved → Execute → Done
                                          ↓
                                      Rejected
```

**CRITICAL**: Posts will NEVER be published without explicit human approval.

## When to Use

- When LinkedIn watcher creates posting opportunity
- For scheduled business content
- To generate sales leads
- For brand awareness campaigns

## Usage

Invoke the skill to draft a new post:

```
/linkedin-drafter
```

Or ask naturally:
```
Draft a LinkedIn post about our business
Create a LinkedIn post for lead generation
```

## Post Templates

Includes three professional templates:
1. **Expertise Post**: Showcases knowledge and thought leadership
2. **Value Proposition Post**: Highlights business value and solutions
3. **Success Story Post**: Shares client results and builds credibility

## Approval Process

1. **Review Draft**: Check `/Pending_Approval` folder
2. **Edit (Optional)**: Modify content directly in the file
3. **Approve**: Move file to `/Approved` folder
4. **Execute**: Run skill again to process approved posts

## Safety Features

- Mandatory approval before posting
- Edit-before-approve capability
- Easy rejection option
- Complete audit trail
- Approval expiration (24 hours)

## Output

- **Draft**: `LINKEDIN_POST_[timestamp].md` in `/Pending_Approval`
- **Execution Log**: `EXECUTED_LINKEDIN_POST_[timestamp].md` in `/Done`
