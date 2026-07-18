---
name: playground-progress-tracker
description: Tracks and displays learning progress across all programming-playground projects at once (one project per technology being learned), reading each project's roadmap.yaml and progress.json, computing statistics, showing an ASCII dashboard per-project or combined across all projects, and recommending which project/milestone to continue next. Use this skill when the user asks "how's my learning progress", "playground dashboard", "what projects am I working on", or "which one should I continue".
metadata:
  version: 1.1.0
---

# Playground Progress Tracker

This skill displays learning progress across all `programming-playground/` projects — each project usually represents one technology being learned (Go, PostgreSQL, Kafka, etc.), each running independently.

This skill is **read-mostly**: actually completing a milestone (changing its status to `completed`) must always go through `playground-session-guide` so every `completed` status has a git commit proving it. This skill may only make small clerical corrections explicitly when the user asks (e.g., a wrongly recorded duration).

## Workspace

The default workspace location is `~/programming-playground/` (read automatically by `scripts/dashboard.py`). If the user uses a different location (e.g., inside a specific project directory), add `--root <path>` to every script invocation in this skill.

## When To Use This Skill

- User asks "how's my learning progress", "playground dashboard"
- User asks "what projects am I working on"
- User asks "which one should I continue" / wants a recommendation
- After `playground-project-architect` or `playground-session-guide` finish their work, those skills already point here on their own — this skill doesn't need to be invoked automatically, only when the user explicitly asks to see progress.

## Instructions

### Step 1: Discover All Projects

```bash
python3 scripts/dashboard.py list
```

This script globs `programming-playground/*/*/progress.json` — there's no separate registry, so it's always up to date with what's actually on disk.

If there are no projects at all, point the user to `playground-project-architect`.

### Step 2: Single-Project Dashboard

If the user asks about one specific technology/project:

```bash
python3 scripts/dashboard.py show <tech>/<slug>
```

Shows an ASCII box: milestone counts per status, total learning time, a progress bar, the current + next milestone (pull a short `why_now` narrative from `roadmap.yaml` for context, not just the id).

See `references/dashboard-format.md` for the exact format.

### Step 3: All-Projects Dashboard

If the user asks about progress in general (without naming a specific technology):

```bash
python3 scripts/dashboard.py list
```

Show a combined table (tech, slug, title, % complete, last session, next milestone) + overall totals (total projects, total milestones completed, total learning time across all projects).

### Step 4: Recommendation

```bash
python3 scripts/dashboard.py recommend
```

Logic (purely state-based, NOT a fixed curriculum — there's no "must learn A before B" ordering):
1. Any project has an `in_progress` milestone → recommend continuing that first (an unfinished session).
2. If none, any project has a `needs_revisit` milestone → recommend a review session.
3. If none, pick the project with the most recent `last_session_at` that still has a `not_started` milestone (momentum — continue what was just touched).
4. A project idle for >14 days (based on `last_session_at`) is flagged as a gentle reminder, not forced to be worked on first.

Deliver the recommendation in Indonesian (the user's conversational language), naturally, with a short reason (e.g., "you're in the middle of milestone m02 in your Go project, let's continue that").

### Step 5: Regenerate the Index

Every time `list` or `show` runs, the script automatically rewrites `programming-playground/README.md` as a side effect (a self-healing index that doesn't depend on another skill to trigger it).

## Rules

### MUST
- Always read `progress.json` as the source of truth for status/statistics (not `roadmap.yaml`, which is only for narrative context).
- Point the user to `playground-session-guide` to actually complete/change a milestone's status.
- Base recommendations purely on project state, never assume a learning order across different technologies.

### MUST NOT
- Never mark a milestone `completed` from this skill without an accompanying git commit — that's `playground-session-guide`'s job.
- Never create an additional registry/index file besides the auto-generated `programming-playground/README.md`.
- Never force a "learn X before Y" ordering across different technologies.

## Quality Checklist

- [ ] The dashboard shows data matching the current `progress.json` contents (not a stale cache)
- [ ] The recommendation names a project + milestone + a short reason
- [ ] `programming-playground/README.md` is updated after the call
