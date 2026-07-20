---
name: playground-project-architect
description: Designs a new learning project for any technology (programming language, database, message broker, etc.) by picking a sufficiently complex project theme, building an ordered roadmap of milestones from basics to mastery grounded in that technology's real concepts (verified via Context7), then scaffolding a runnable project skeleton (git init, README, roadmap.yaml, progress.json) inside programming-playground/<tech>/<project-slug>/. Use this skill when the user says "I want to learn <technology>", "start a learning project for <technology>", "make a playground project for <technology>", or asks for a curriculum/roadmap to be designed for a new technology with no existing project.
metadata:
  version: 1.2.0
---

# Playground Project Architect

This skill designs a new learning project for any technology (programming language, database, message broker, infra tool, etc.), following a **project-based playground** philosophy: not a tutorial made of disconnected code snippets, but ONE real project that grows from a small skeleton into something more complex as concepts are learned. Each concept is later implemented directly into this project by the companion skill, `playground-session-guide`.

This skill ONLY handles the initial design (theme + roadmap + scaffold). To run a learning session on an existing project, use `playground-session-guide`. To see progress across all projects, use `playground-progress-tracker`.

## Workspace

All learning projects are stored in the `programming-playground/` workspace directory. The default is `~/programming-playground/` (the user's home directory). Before using this default:
1. Check whether the user already has a `programming-playground/` folder elsewhere (e.g., inside the project directory currently open) — if so, use that.
2. If the user has previously mentioned a custom location, use it consistently.
3. If there's no indication either way, use `~/programming-playground/` and tell the user the location.

For the rest of this skill, `<PLAYGROUND_ROOT>` refers to this directory.

## When To Use This Skill

- User says "I want to learn Go/Rust/PostgreSQL/Kafka/etc"
- User asks to "make a playground project for X"
- User asks for a roadmap/curriculum to be designed for a new technology
- **Not** for continuing an existing project (that's `playground-session-guide`'s job) — always check Step 1 first

## Instructions

### Step 1: Clarify Scope & Check for an Existing Project

Before designing anything:

1. Check whether a project already exists for this technology: `ls <PLAYGROUND_ROOT>/<tech-slug>/` (also glob `*/progress.json` to see all existing projects).
2. **If a project already exists for this tech** — don't scaffold a new one. Tell the user the project already exists, offer to continue with `playground-session-guide`, or (only if the user explicitly wants a SECOND project for the same tech, e.g. to experiment with a different theme) proceed with a different project slug.
3. Gather the following info (use `AskUserQuestion` if not already clear from the request):
   - Technology name & version (e.g., "Go 1.22", "PostgreSQL", "Kafka")
   - The user's experience level with this technology (total beginner / tried it a little / experienced in other languages but new to this one)
   - Project domain preference if any (e.g., "I like building things related to e-commerce") — if there's no preference, move to Step 3 to propose one.
4. Ask how the **m00 skeleton** should be created, via `AskUserQuestion`, unless the user already stated a preference:
   - **Build fully from scratch (default/recommended)** — Claude does NOT write any working code upfront. Only the technology's bare init command runs (e.g., `go mod init`, `cargo init`), with no logic implemented. `m00` stays `not_started` in `progress.json`, exactly like every other milestone, and gets taught as the project's first real `playground-session-guide` session (theory → hint/pair-programming → the user writes the first lines of code themselves). This avoids handing the user a working `net/http` server (or equivalent) before they've learned any of it.
   - **Scaffold by AI** — Claude researches, writes, and verifies a working `m00` skeleton immediately (the previous default behavior). Useful when the user just wants a ready base to extend and prefers to learn starting from `m01` onward.

   Record the choice; it drives Step 5 below and is passed to `scaffold_project.py` as `--skeleton-mode`.

### Step 2: Research via Context7

Before designing a theme or roadmap, research the technology first:

1. `resolve-library-id` for the main technology (and 1-2 ecosystem libraries likely to be used, e.g., a database driver, a client library).
2. `query-docs` to understand:
   - The idiomatic project structure for this technology
   - Standard tooling (build tool, test framework, package manager)
   - **Flagship/distinctive features** of this technology — important because these become the roadmap's eventual target (e.g., Go is known for goroutines/channels; PostgreSQL for indexing/transactions/JSONB; Kafka for partitioning/consumer groups/delivery guarantees)

Keep a concise record of these findings — they'll be noted in `roadmap.yaml` as `context7_libraries_consulted`.

### Step 3: Choose the Project Theme

See `references/project-theme-heuristics.md` for detailed heuristics. In short:

1. Work **backward from the technology's flagship features** (from Step 2's research), not forward from a generic app idea. The project theme must have a natural path toward those features.
2. Check the sizing: the initial skeleton (`m00`) should run in under 30 minutes, but the project needs a natural extension point toward complexity (don't go as trivial as "hello world", nor as broad as "a full SaaS platform").
3. Draft 1-2 concrete theme options and **confirm with the user** via `AskUserQuestion` before designing the full roadmap — don't decide unilaterally.

### Step 4: Design the Roadmap

See `references/roadmap-template.md` for the full schema and examples. In short:

1. Brainstorm a list of concepts from basics → mastery based on Step 2's research, leading toward that technology's flagship features.
2. Group them into **8-15 milestones**, each covering 1-3 related concepts, estimated at 30-90 minutes of work.
3. Every milestone MUST have a `why_now` field: a CONCRETE limitation/need in the project's current state that only this milestone's concept can resolve. This is the core of the "project-based" philosophy — not "now let's learn X" but "our project needs X because Y".
4. Sequencing: `m00` = a runnable skeleton. Then a repeating pattern: **add a feature the naive way → that feature turns out to be problematic/limited under realistic conditions → learn the concept that fixes it**. Close with 1-2 quality milestones (testing, error handling, observability) so the project always ends in a presentable state.
5. Every milestone has `prerequisites` (a list of milestone ids that must be completed first).

### Step 5: Scaffold the Project

1. Determine the `tech-slug` (kebab-case, e.g., `go`, `postgresql`, `rabbitmq`) and `project-slug` (kebab-case from the theme, e.g., `url-shortener`).
2. Project path: `<PLAYGROUND_ROOT>/<tech-slug>/<project-slug>/`. Make sure it doesn't already exist.
3. Branch on the skeleton-mode choice from Step 1:

   **Build from scratch (default)**:
   - Run ONLY the technology's bare init/dependency-manager command via Bash — e.g., `go mod init <module>`, `cargo init`, `npm init -y` — whatever creates the minimal project manifest for that technology. **Do not write any handler/server/connection logic, do not create a working entrypoint.** At most leave the empty/stub entrypoint the init command itself generates (e.g., `cargo init`'s placeholder `main.rs`) — Claude must not add to it.
   - Skip the "verify it runs" check — there's nothing meaningful to run yet.
   - Pass `--skeleton-mode scratch` (or omit `--skeleton-mode`, since it's the script's default) and omit `--run-command`.

   **Scaffold by AI**:
   - **Run the technology's actual init command directly via Bash** (not hardcoded in a generic script) — e.g., `go mod init <module>`, `cargo init`, `npm init`, etc. — based on Step 2's research. Create an `m00` skeleton that genuinely runs (e.g., a "hello world" HTTP server, a basic DB connection).
   - **Verify the skeleton actually runs** (run/build) before proceeding.
   - Pass `--skeleton-mode ai` and `--run-command "<command to run m00>"`.
4. Run the scaffold meta-files script:
   ```bash
   python3 scripts/scaffold_project.py \
     --project-dir "<PLAYGROUND_ROOT>/<tech-slug>/<project-slug>" \
     --tech "<tech-slug>" --slug "<project-slug>" --title "<project title>" \
     --skeleton-mode <ai|scratch> [--run-command "<command>"] \
     --roadmap-json '<the roadmap JSON designed in Step 4>'
   ```
   This script writes `roadmap.yaml` (including `project.skeleton_mode`), `progress.json`, `README.md`, runs `git init` + an initial commit, and regenerates the `programming-playground/README.md` index.
   - In `ai` mode, `m00` is immediately marked `completed` in `progress.json` since the skeleton was already verified to run.
   - In `scratch` mode, `m00` stays `not_started` like every other milestone — `playground-session-guide` will teach and build it as the project's first session.
5. For the JSON roadmap format the script expects, see `references/roadmap-template.md`, section "JSON Schema for scaffold_project.py".

### Step 6: Wrap-up

1. Summarize the roadmap narratively to the user (in Indonesian, the conversational language): the project theme, why this theme fits this technology, a short milestone list.
2. Point the user to `playground-session-guide` to continue:
   - **Scratch mode**: the first session will build `m00` itself (from an empty/init-only project) — say so explicitly, so the user knows the very first session starts from nothing.
   - **AI mode**: the first session starts at `m01`, since `m00` is already done.
3. Mention `playground-progress-tracker` for checking the dashboard anytime.

## Rules

### MUST
- Research via Context7 BEFORE designing the theme/roadmap — don't rely on training-data knowledge for version-specific details.
- Every milestone has a concrete `why_now`, tied to the project's state, not a generic explanation.
- Confirm the theme with the user before designing the full roadmap (one round-trip, don't drag it out).
- Ask the skeleton-mode question (Step 1.4) before scaffolding — default to **build from scratch** if the user has no preference; never silently assume AI-scaffold.
- In AI mode: verify the `m00` skeleton genuinely runs before the scaffold is considered done.
- In scratch mode: only run the technology's bare init command — never write handler/logic code into `m00`, that belongs to the first `playground-session-guide` session.
- Check for an existing project first before scaffolding (Step 1) — don't overwrite an existing project.

### MUST NOT
- Never use a hardcoded/fixed curriculum template — every technology's curriculum is redesigned from its own Context7 research.
- Never make the `m00` skeleton exceed its own scope (other milestones' features must not be implemented upfront) — this applies doubly in scratch mode, where `m00` should contain no logic at all.
- Never pick a project domain that's too trivial (will never need advanced features) or too broad (its skeleton will never be finished).
- Never re-scaffold a project for a tech that already has one without explicit confirmation from the user.

## Quality Checklist

Before declaring the project ready:
- [ ] Context7 research has been done and recorded in `roadmap.yaml`
- [ ] The theme has been confirmed with the user
- [ ] The skeleton-mode choice (scratch/ai) has been asked and recorded
- [ ] 8-15 milestones with a concrete `why_now` per milestone
- [ ] AI mode: the `m00` skeleton genuinely runs (tested). Scratch mode: only the bare init command ran, no logic was written.
- [ ] `roadmap.yaml`, `progress.json`, `README.md` are written
- [ ] The git repo is initialized with an initial commit
- [ ] The `programming-playground/README.md` index is updated
