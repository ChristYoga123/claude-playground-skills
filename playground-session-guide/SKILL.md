---
name: playground-session-guide
description: Guides a single real learning session inside an existing playground project — reads the project's roadmap.yaml and progress.json, determines the next milestone, explains the concept grounded in a real limitation currently present in the project's code (not a separate code example), implements that concept directly in the project's source code (pair-programming or hint/self-practice mode), then commits per milestone with a message referencing the concept learned. Use this skill when the user says "continue learning <tech>", "continue playground project", "teach me <concept> in this project", or wants to resume a learning session already in progress.
metadata:
  version: 1.6.0
---

# Playground Session Guide

This skill runs ONE real learning session inside a playground project already created by `playground-project-architect`. Philosophy: the concept being taught MUST connect to a concrete limitation that genuinely exists in the project's code right now — not a generic explanation that happens to be implemented in this project.

If no project exists yet for the requested technology, redirect to `playground-project-architect` first. To see progress across all projects, redirect to `playground-progress-tracker`.

## Workspace

All learning projects live in the `programming-playground/` workspace directory (default `~/programming-playground/`, or another location the user has already used before — check existing projects with a `**/progress.json` glob if unsure). In this skill, `<PLAYGROUND_ROOT>` refers to that directory.

## When To Use This Skill

- User says "continue learning Go/Rust/etc" or "continue playground project"
- User asks to be taught a specific concept in a project already in progress
- User wants to resume a session that was interrupted (milestone with status `in_progress`)

## Instructions

### Step 1: Locate the Project

1. If the user explicitly names a technology/project, look it up at `<PLAYGROUND_ROOT>/<tech>/<slug>/`.
2. If ambiguous (multiple matching projects, or none named), glob `<PLAYGROUND_ROOT>/*/*/progress.json`, show a short list, and ask via `AskUserQuestion` — or if the user just says "continue learning" with no specifics, recommend the project with the most recent `last_session_at`.
3. If no project exists at all for the requested technology: tell the user and redirect to `playground-project-architect`. **Do not** improvise a new project from this skill.

### Step 2: Load State

1. Read `roadmap.yaml` (full narrative) and `progress.json` (machine status) for that project.
2. Determine the next milestone: prioritize any milestone with status `in_progress` (resume an interrupted session) → then `needs_revisit` milestones if the user explicitly asks for a review → then the first `not_started` milestone whose `prerequisites` are all `completed`.
3. If the user explicitly requests a different milestone/concept (out of default order), honor that — but check its prerequisites are met first; if not, say so and confirm whether to proceed anyway.

### Step 3: Choose the Reference Material Source (once per session)

Before explaining the first milestone in this session, ask the user via `AskUserQuestion` which reference source to use for theory throughout this session:

- **AI does the research** (default) — Claude researches via Context7 as usual (proceed to Step 4).
- **I'll provide my own reference** — the user can type material/points directly in chat, OR provide a path to a local file / a URL they've already prepared. If it's a local file, `Read` it; if it's a URL, `WebFetch` it. This material becomes the primary basis for the theory explanation in Step 4 — Context7 may still be used as a supplement when the user's reference doesn't cover a specific technical/API detail that's needed.

**Skip this question** (use the default AI-research path directly) when:
- The user already stated a preference explicitly at the start of this session's request (e.g., "just use the material from this file", "explain it in the style of book X").
- This session is continuing a session where the question was already asked (the choice has already been made — don't re-ask every time the user says "continue").

This preference applies to the **entire session** (every milestone worked on until this conversation ends), not per milestone — it doesn't need to be written to `progress.json`, just remembered for the conversation. If the user changes their mind mid-session (e.g., asks to switch from AI to their own reference), follow that change starting with the next milestone.

### Step 4: Ground the Concept in a Real Pain Point

This is the most important step — don't teach straight from `why_now` in `roadmap.yaml` verbatim, that's only an initial hypothesis:

1. Read the project's current source code (the relevant files, not just the README) to find/confirm the concrete limitation — name the specific function/line that will break without this milestone's concept.
2. When possible, **reproduce the problem live** before teaching the solution: run the program, show the actual race condition/error/slow query/etc. happening. This makes the concept's effect feel concrete, not abstract.
3. Per the Step 3 choice: if the reference source is "AI research", query **Context7** for the specific concept/API being taught right now — don't rely solely on the architect's research, which may be somewhat generic; verify the current idiomatic approach. If the reference source is "from the user", base the explanation on the material the user provided (still fine to cross-check Context7 for technical details the user's material doesn't cover).
4. Explain the concept in Indonesian (the language the user prefers to converse in), with an analogy where it helps, always tied back to the real limitation just demonstrated.

See `references/teaching-mode-guide.md` for example dialogue and how to frame the explanation.

### Step 5: Write Full Notes to the `notes/` Folder (BEFORE giving the task)

As soon as the Step 4 theory has been explained — before giving the user a task/hint — write full notes to a separate file in the project. The goal is a **standalone written guide the user can keep open while working**, not a thin summary that just repeats the chat.

1. Create a `notes/<milestone-id>-<slug>/` folder at the project root if it doesn't exist yet (e.g., `notes/m01-var-const/`, `notes/m08-channel-waitgroup/`). Create the parent `notes/` folder too if the project doesn't have one.
2. Write `notes/<id>-<slug>/README.md` in English, structured as:
   - **Title & concepts** — a list of the technical terms covered.
   - **Full explanation** — definition, why the concept exists, when it's used. Feel free to (and are encouraged to) use **standalone dummy/generic examples** (not necessarily from this project) when that makes the concept clearer before diving into the project's context. Write simply but with detail, avoid unexplained jargon.
   - **Code block** for each example (both dummy and real snippets from the project).
   - **Diagram** — use Mermaid (```mermaid) when the concept has a flow/structure that's easier to grasp visually. **Required** for concurrency concepts (goroutine, channel, select, worker pool, context) — illustrate the data flow between goroutines/channels using `sequenceDiagram` or `flowchart` (e.g., which goroutine sends to which channel, when `select` picks which branch). For struct/pointer concepts, a memory-reference diagram (who points to what) also helps a lot. For purely syntactic concepts (basic var/const) a diagram is optional — don't force one if it doesn't add clarity.
   - Final section **`## Task In This Project`** — only here does it tie back to the project's real pain point from Step 4 (the specific function/file to change), with a bit of progressive guidance (not the full solution — follow the hint tiers in `references/teaching-mode-guide.md` for hint mode).
3. Update the project's root `README.md`: the `## Learning Notes` section should just be a **list of links**, don't duplicate the full content there:
   ```markdown
   ## Learning Notes
   - [m01: Proper var declarations & constants](./notes/m01-var-const/README.md)
   ```
4. The "Task In This Project" section is written prospectively (the condition CURRENTLY being fixed) since the task isn't done yet when this is written. If the user's final implementation diverges from the plan, revise that section as needed in Step 8 before committing — the theory/diagram sections above it usually don't need to change since they don't depend on the user's specific implementation.

### Step 6: Choose the Session Mode

The default mode is **hint / self-practice** — this skill is designed like a coding-playground website: the user types the code themselves to get comfortable with the syntax, rather than Claude writing it. Use this mode directly without asking, except when:

- The user has already stated an explicit different preference at the start ("let's do pair-programming", etc.).
- `progress.json` already recorded a `mode` for the milestone being resumed — continue with the same mode.
- The context clearly calls for pair-programming (e.g., the concept is too setup-heavy/boilerplate for self-practice, or the user explicitly asks to see an example first) — in this case, offer it via `AskUserQuestion` instead of switching modes automatically.

- **Hint / self-practice** (default): Claude STILL explains the concept's underlying theory first (what it is, why it exists, basic syntax/semantics — as thorough as pair-programming, see Step 4), then gives the task + the limitation to fix + a bit of guidance on how to approach it in this project (not the full solution), then progressively deeper hints if still stuck (see `references/teaching-mode-guide.md` for the tier mechanism). The user tries it themselves first, Claude reviews the result (reads the file + runs tests/build), gives feedback, and only writes code if the user is stuck or asks for it. **Hint mode does not mean leaving the user without theory** — the difference from pair-programming is in who types the code, not in how thoroughly the concept is explained.
- **Pair-programming**: Claude explains the concept, then implements it directly in the project files while explaining each change.

Save the chosen mode to `progress.json` (via `update_progress.py start`, see Step 10).

### Step 7: Real Implementation

- Changes MUST land in the actual project files — extend existing functions/structures, DO NOT create a separate demo file disconnected from the main application.
- In hint/self-practice mode: once the user submits their work, `Read` the changed file, compare it against expectations, and give concrete feedback referencing specific lines/functions.

### Step 8: Verify

1. Run the project's build/test/run to prove the concept works.
2. Re-run the Step 4 pain-point reproduction (if any) to show the problem is now resolved — this is an important part of "closing the loop" on the learning.
3. Double-check the `## Task In This Project` section in `notes/<id>-<slug>/README.md` written in Step 5 — if the user's final implementation diverged from what was planned when the theory was explained, revise that section as needed to keep it accurate.

### Step 9: Commit per Milestone

1. Stage ONLY the files relevant to this milestone.
2. Commit using the format from `references/commit-message-convention.md`:
   - Subject: `<milestone-id>: <concept summary>` (English, consistent with the `title` in the roadmap)
   - Body: explain the pain point fixed + what was learned (in English)
   - Trailer: `Milestone-Id: <id>`
3. **Hard rule: one clean commit per completed milestone.** Never commit a broken/half-finished state as a milestone commit.
4. If the session is interrupted before a milestone is finished: DO NOT commit the WIP state. Leave the working tree as-is, record status `in_progress` with `notes` explaining the last progress made (via `update_progress.py start` with `--notes`), so the next session can resume clearly.

### Step 10: Update `progress.json`

```bash
python3 scripts/update_progress.py complete \
  --project "<PLAYGROUND_ROOT>/<tech>/<slug>" \
  --milestone <id> --commit <sha> --duration <minutes> --mode <pair|hint> \
  --notes "<short summary in English>"
```

To start/mark a session that isn't finished yet:
```bash
python3 scripts/update_progress.py start \
  --project "<path>" --milestone <id> --mode <pair|hint> --notes "<resume notes>"
```

For milestones that need to be redone or skipped, see the `revisit` and `skip` subcommands (full docs in the script's help: `python3 scripts/update_progress.py --help`).

### Step 11: Close the Session

1. Summarize what was just learned and how it changed the project.
2. Give a short teaser of the next milestone's `why_now` (make it intriguing, don't fully spoil it).
3. Mention `playground-progress-tracker` if the user wants to see the overall dashboard.

## Edge Cases

- **Scope creep found mid-session** (e.g., the user wants to explore something outside the roadmap): offer to add a new milestone to `roadmap.yaml` (edit directly, insert at a sensible position) and to `progress.json` (via `update_progress.py append-milestone`), with `why_now: "discovered during a learning session"`. Confirm with the user before adding.
- **Revisiting an already-`completed` milestone**: use the commit prefix `revisit(<id>): <summary>` to distinguish it from the original milestone commit, then `update_progress.py revisit`.

## Rules

### MUST
- Ground the explanation in the project's ACTUAL code, not a generic example — read first, then explain.
- Explain the concept's underlying theory in full BEFORE giving a hint/task, in any mode (including hint/self-practice) — don't jump straight to "try to figure out which concept applies" without teaching the theory first.
- Write full notes (theory + examples + diagram if relevant + task) to `notes/<id>-<slug>/README.md` BEFORE giving the task to the user (Step 5), not after it's done — so it becomes a written guide the user can open while working. The project root `README.md` should just link to it; don't let the explanation live only in chat.
- Include a Mermaid diagram in the notes for concurrency concepts (goroutine/channel/select/worker pool/context) so the data flow is visible, not just text.
- Ask about the reference material source (AI research vs. the user's own reference) once at the start of the session (Step 3), unless it's already clear from the user's request context or this is a continuing session where it was already asked.
- Verify the solution via Context7 for the specific concept being taught right now (unless the user chose their own reference — in that case Context7 becomes a supplement, not the primary source).
- One clean commit per completed milestone, with a consistent format and trailer.
- Update `progress.json` via `update_progress.py`, not manual edits (to keep timestamps & state transitions consistent).
- Ask about the session mode (pair vs. hint) unless it's already clear from context.

### MUST NOT
- Never commit a WIP/broken state as a milestone commit.
- Never create a separate demo file — all implementation goes into the main project.
- Never skip Step 4 (grounding in a real pain point) — this is what distinguishes this skill from a regular tutorial.
- Never improvise a new project from this skill — that's `playground-project-architect`'s job.
- Never re-ask about the reference material source every milestone within the same session — just once at the start (Step 3).

## Quality Checklist

- [ ] The concept is explained by referencing the project's real code/limitation (not generic)
- [ ] The reference material source (AI/user) has been confirmed at the start of the session
- [ ] Context7 has been checked for this specific concept (or the user's reference was used as the primary basis)
- [ ] The session mode (pair/hint) has been confirmed
- [ ] The implementation landed in real project files, verified to work (build/test/run)
- [ ] `notes/<id>-<slug>/README.md` contains full theory + examples + task (and a Mermaid diagram if the concept is concurrency/structural), and the root `README.md` links to it
- [ ] One clean commit with a message following the convention
- [ ] `progress.json` updated via the script (not manually)
