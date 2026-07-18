# ASCII Dashboard Format

## Single-Project (`dashboard.py show <tech>/<slug>`)

```
+============================================================+
|  Learning Dashboard: Hello Test (go)                        |
+============================================================+
|                                                              |
|  Completed     : 2 milestone                                |
|  In Progress   : 0 milestone                                |
|  Needs Revisit : 0 milestone                                |
|  Not Started   : 1 milestone                                |
|                                                              |
|  Total Time    : 0h 25m                                     |
|  Progress      : [######____] 66%                           |
|                                                              |
+--------------------------------------------------------------+
|  Next Milestone: m02 - Extra concept                         |
|  discovered during a session                                 |
|                                                              |
|  Last Session: 2026-07-18                                   |
+============================================================+
```

Progress bar: 10 characters, `#` for filled (percent complete), `_` for the remainder.

## All-Projects (`dashboard.py list`)

```
Programming Playground - All Learning Projects
================================================================

Tech   Slug           Title                Progress    Last Session  Next
------ -------------- -------------------- ----------- -------------- --------------------------
go     hello-service  Hello Test           2/3 (66%)   2026-07-18     m02: Extra concept
postgresql  order-db  Order Processing DB  1/10 (10%)  2026-07-15     m01: Design orders schema

Total: 2 projects, 3/13 milestones completed (23%), 25 minutes learned
```

## Recommendation (`dashboard.py recommend`)

Short text format, example:

```
Recommendation: continue milestone m02 (Extra concept) in project go/hello-service
  -> this session is still in_progress from before.

Reminder: project postgresql/order-db hasn't been touched in 16 days.
```

If there's no `in_progress`/`needs_revisit`, the shape is:
```
Recommendation: continue project go/hello-service (most recent activity), milestone m02: Extra concept
  why_now: discovered during a learning session
```

> Note: this is the raw script output. When relaying it in chat, Claude presents the recommendation naturally in Indonesian (the user's conversational language), per `playground-progress-tracker/SKILL.md` Step 4.
