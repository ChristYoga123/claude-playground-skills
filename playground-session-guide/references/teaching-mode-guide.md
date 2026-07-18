# Session Mode Mechanics & Example Dialogue

> Note: the example dialogue below is written in English for documentation purposes. In actual sessions, Claude converses with the user in Indonesian (the user's preferred language), while code and technical terms stay in English.

## Pair-Programming Mode

Flow: explain → implement → verify together. Good for concepts that are genuinely new to the user or when the user wants fast progress.

Example flow:

> "Right now in `store.go`, the functions `Get()` and `Set()` access the `urls` map directly with no protection at all. If I run `go test -race ./...` now..."
>
> *(run the test, show the race detector firing)*
>
> "This is what's called a race condition — two goroutines reading and writing the same map at the same time produce undefined results and can crash. The fix is to use `sync.Mutex` to lock access to this map. Let me add that now in `store.go`..."
>
> *(edit the file, explain each changed line)*
>
> "Now let's run the race detector again..."
>
> *(re-run, show it's clean now)*

## Hint / Self-Practice Mode

Flow: describe the task + limitation → tiered hints (progressive reveal) → user tries it themselves → review → feedback.

### Hint Tiers

**Required before Tier 1: the concept's underlying theory.** Hint mode is NOT "figure it out yourself with no explanation" — the user still needs to be taught the theory (what it is, why it exists, basic syntax/semantics) just like in pair-programming mode, with an analogy when it helps. The difference from pair-programming is only in who types the code, not in how deeply the theory is explained. This is part of Step 4 (grounding in the pain point) and must appear BEFORE Tier 1 is given, not folded into a single question.

Example of the full sequence for the race-condition case above:

> **Theory first:** "In Go, when multiple goroutines read and write the same data concurrently without protection, that's called a *race condition* — the result is undefined and the program can crash or produce wrong data without a clear error. Go has several ways to protect shared data, one of them is `sync.Mutex`: a 'lock' that only one goroutine can hold at a time. A goroutine that wants to access the data calls `Lock()` first (waiting if another goroutine currently holds it), then `Unlock()` when done."
>
> **Tier 1 — Task direction + a bit of guidance** (given right after the theory, don't split it into a separate turn):
> "Now look at the `Get()` and `Set()` functions in `store.go` — both access the `urls` map without this protection. Your task: add that protection to the `Store` struct and use it in both functions. A small nudge so you don't get stuck: the lock usually becomes a field in the same struct as the data it protects, and gets locked/unlocked at the start/end of every function that touches that data."

**Tier 2 — API shape** (if the user asks for another hint / looks stuck):
> "More specific hint: the `sync` package has a `Mutex` type with `Lock()` and `Unlock()` methods. Try adding it as a field in the `Store` struct, then call it at the start/end of every method that accesses the map."

**Tier 3 — Full solution** (only if explicitly requested — "show me the solution" — or the user has tried and is still stuck):
> Show the complete code with an explanation of each part.

**Tier rule**: don't jump to tier 3 before the user genuinely asks for it or has tried and failed. Progressive, not an immediate answer. But the base theory is NOT part of this progression — it always appears first, in full, at every tier.

### Reviewing the User's Work

1. `Read` the file the user changed.
2. Run build/test for objective verification.
3. Give feedback referencing specific lines/functions — acknowledge what's correct, explain why anything wrong is wrong, tie it back to the concept.
4. If the user misunderstood the core concept (not just a typo), offer a short re-explanation before moving on, or mark the milestone `needs_revisit` if it still isn't clicking after a few attempts.

## When to Choose Which Mode (Question Guide)

The global default is **hint / self-practice** — use it directly without asking. Except when:
- The concept is genuinely new/unfamiliar and setup-heavy (lots of boilerplate unrelated to the core concept) → it's fine to offer pair-programming via `AskUserQuestion`, with a short reason why.
- The user explicitly requests a specific mode → honor it directly without re-asking.
- `progress.json` already recorded a mode for the milestone being resumed → continue with the same mode.
