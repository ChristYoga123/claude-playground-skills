# Per-Project `README.md` Template

Written directly by Claude (via `scaffold_project.py`) during scaffolding; may be updated manually by `playground-session-guide` as the project evolves (e.g. updating the "Running It" section when a new dependency is added).

```markdown
# {Project Title}

> A **{tech}** learning project created via `playground-project-architect`.
> Progress: see `progress.json` or run `playground-progress-tracker`.

## Theme

{theme_rationale, 2-4 sentences}

## Running It

```bash
{tech-specific run/build command, e.g. `go run .` or `cargo run`}
```

## Learning Structure

The full roadmap is in [`roadmap.yaml`](./roadmap.yaml). Progress and status for each milestone is in [`progress.json`](./progress.json).

To continue a learning session, use the `playground-session-guide` skill.

## Learning Trail (Git Log)

Each completed milestone is its own commit — run `git log --oneline` in this folder to see the sequence of concepts learned.
```

Placeholders `{tech}`, `{theme_rationale}`, and the run command are filled in by `scaffold_project.py` based on the arguments it receives from SKILL.md Step 5.
