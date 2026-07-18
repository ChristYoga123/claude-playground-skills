# Per-Milestone Commit Convention

## Format

```
<milestone-id>: <short concept summary, English>

<body: 1-3 sentences in English, explain the pain point fixed
and what was learned>

Milestone-Id: <milestone-id>
```

## Example

```
m02: Add mutex to protect concurrent map access

Store.Get()/Set() previously raced when accessed by many goroutines at
once (clearly visible with `go test -race`). Now protected by sync.Mutex.

Milestone-Id: m02
```

Revisit example:
```
revisit(m02): Re-explain mutex vs RWMutex tradeoff

Milestone m02 was revisited because it was still unclear when to use
RWMutex vs a plain Mutex. Added RWMutex plus a comparison benchmark.

Milestone-Id: m02
```

## Rules

- First-line subject: `<id>: <milestone title>` or a clear summary if slightly different from the roadmap's `title` — always in English so `git log --oneline` stays consistent and reads well as a technical trail.
- Body is written in English; technical terms/function names stay as-is.
- The `Milestone-Id: <id>` trailer is REQUIRED — used by `playground-progress-tracker` and `git log --grep "Milestone-Id: m02"` for quick lookup.
- One milestone = one commit. If multiple exploratory commits pile up while trying things out, squash them into one before finishing the milestone, or use `git commit --amend` as long as you haven't moved on to the next milestone.
- Never mix changes from two different milestones in one commit.

## How to Make the Commit (Bash example)

```bash
git add <files relevant to this milestone>
git commit -m "m02: Add mutex to protect concurrent map access" -m "Store.Get()/Set() previously raced when accessed by many goroutines at once (clearly visible with \`go test -race\`). Now protected by sync.Mutex.

Milestone-Id: m02"
```

Grab the short SHA afterward to record in `progress.json`:
```bash
git rev-parse --short HEAD
```
