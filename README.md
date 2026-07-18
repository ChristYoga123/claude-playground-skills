# Claude Playground Skills

> Created by [@znmn](https://github.com/znmn)

Three cooperating [Claude Code Skills](https://docs.claude.com/en/docs/claude-code/skills) for learning a programming language or other technology (database, message broker, infra tool, etc.) through **project-based playground** learning: instead of a tutorial with disconnected, dummy code examples, you build one real project that grows from a small skeleton into something complex as you learn each concept — every concept is implemented directly inside that same project, so you always see its actual use case and effect on your own codebase.

## Philosophy

Conventional learning often goes: read the theory of goroutines → look at a 10-line standalone example → forget it again next week because you never saw its effect on anything real.

These skills flip that around: you start with a small project (e.g. a URL shortener to learn Go), and every new concept shows up because your project **actually needs it** — the server starts receiving lots of concurrent requests? Time to learn goroutines & mutexes. Redirects getting slow because you always hit storage? Time to learn caching. The concept sticks because you see its effect directly in code you wrote yourself, and your project's git log becomes a traceable learning trail.

## The Three Skills

| Skill | When It's Used |
|---|---|
| [`playground-project-architect`](./playground-project-architect) | Start learning a new technology — research it via Context7, design a project theme + milestone roadmap, scaffold a real working project. |
| [`playground-session-guide`](./playground-session-guide) | Continue a learning session on an existing project — teach the next concept grounded in a real limitation of the current code, implement it, commit per milestone. |
| [`playground-progress-tracker`](./playground-progress-tracker) | See progress across all learning projects, get a recommendation on which project/milestone to resume. |

Full details are in each folder's `SKILL.md`.

## Installation

Claude Code reads skills from your personal skills directory:

```bash
git clone https://github.com/znmn/claude-playground-skills.git
cp -r claude-playground-skills/playground-project-architect \
      claude-playground-skills/playground-session-guide \
      claude-playground-skills/playground-progress-tracker \
      ~/.claude/skills/
chmod +x ~/.claude/skills/playground-*/scripts/*.py
```

Claude Code will pick up the skills automatically in your next session (verify by naming a skill directly, or by triggering one of its description's trigger phrases).

## Workspace

All three skills agree on a single workspace directory (`programming-playground/`) where every learning project is stored, one subfolder per technology:

```
~/programming-playground/            <- default, can be changed
  <tech-slug>/                       <- e.g. go, rust, postgresql, kafka
    <project-slug>/                  <- e.g. url-shortener
      .git/                          <- its own git repo per project
      README.md
      roadmap.yaml                   <- narrative design: theme, milestones, rationale per concept
      progress.json                  <- machine state: status/timestamp/commit sha per milestone
      <project source code>
```

The default location is `~/programming-playground/`. If you want a different location, just tell Claude when you start ("put it in ~/dev/learning"), or pass `--root <path>` when calling `playground-progress-tracker` manually.

## Example Usage

```
You: I want to learn Go
Claude: [playground-project-architect] researches via Context7, proposes a "URL
        shortener with caching & rate limiting" theme, designs 9 milestones,
        scaffolds a working project.

You: let's continue learning Go
Claude: [playground-session-guide] reads the current code, demonstrates a real
        race condition under load, teaches goroutines + mutexes, implements it,
        commits milestone m02.

You: what's my learning progress?
Claude: [playground-progress-tracker] shows a dashboard across all projects +
        a recommendation on what to resume.
```

## Content Conventions

- Concept explanations/narration inside the skills: Bahasa Indonesia (the author's teaching language).
- Code, technical terms, field names, commit messages: English.
- One clean git commit per completed milestone, with a `Milestone-Id: <id>` trailer.
- All Python scripts are stdlib-only — no external dependencies to install.

## License

MIT — see [LICENSE](./LICENSE).
