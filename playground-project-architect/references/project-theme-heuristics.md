# Heuristics for Choosing a Project Theme

Goal: pick ONE project theme complex enough to naturally require the flagship features of the technology being learned, without being so broad that its initial skeleton never gets finished.

## Core Principle: Work Backward From the Flagship Features

Don't start from "a cool app idea" — start from "what feature makes this technology special" (the Context7 research from Step 2), then find a project domain that **needs** that feature to work correctly — not one that can merely use it optionally.

Example of CORRECT reasoning:
- Research: Go is known for goroutines, channels, and lightweight concurrency primitives.
- A domain that naturally needs this: a service that must handle many concurrent requests/connections (a high-traffic URL shortener, a chat server, a parallel web scraper, a task queue worker).
- A domain that does NOT fit: a simple CLI calculator (never needs concurrency to work correctly).

Example of INCORRECT reasoning:
- "I like to-do list apps, so let's build a to-do list in Go" — then goroutines get bolted on as an unnatural add-on feature.

## Heuristics by Technology Category

**Programming languages (Go, Rust, async Python, etc.)**
→ Small-to-medium networked/concurrent services: a URL shortener with caching, a chat server, a job queue/worker pool, a plugin-based CLI, a parallel web scraper with rate limiting.
→ Why: modern languages usually excel at I/O, concurrency, and error handling — all of which only feel useful under a real workload (many requests/connections/goroutines).

**Relational databases (PostgreSQL, MySQL, etc.)**
→ Applications with a growing schema and increasing query load: a product catalog + orders (mini e-commerce), a multi-warehouse inventory system, a social feed with follow/like.
→ Why: indexing, transactions, JSONB/full-text search, replication, and query optimization only start to feel necessary once the data and its relations are complex enough — not a single table.

**NoSQL / key-value / cache databases (Redis, MongoDB, etc.)**
→ Applications needing fast repeated access or flexible data structures: a real-time leaderboard, a session store, a rate limiter, a feed with a frequently changing schema.

**Message brokers (Kafka, RabbitMQ, NATS, etc.)**
→ Event-driven pipelines: order processing (order placed → payment → shipping → notification), notification fan-out, log aggregation.
→ Why: a broker only shows its value (partitioning, consumer groups, delivery guarantees, dead-letter queues) when there are multiple independent consumers/producers and realistic failure scenarios.

**Infra/DevOps tools (Docker, Kubernetes, Terraform, etc.)**
→ Deploy & operate one of the projects above — infra tools always need a real workload to practice on; don't make an "empty" project that's just configuration with no running application inside it.

## Size Check Before Finalizing

1. **`m00` skeleton < 30 minutes**: it can be scaffolded and run (even if still very simple) quickly. If the initial setup alone takes hours, the theme is too big.
2. **A natural path to advanced features exists**: quickly map the 3-5 flagship features from the research to which part of the project will need them. If a flagship feature has no natural place in this theme, consider a different theme or expand the scope a bit.
3. **Not infinite-scope**: the project needs a clear "done" point (e.g., "an end-to-end order-processing system with retry & dead-letter queue") — not a "do-everything platform" that can be expanded forever.

## Confirming With the User

Once 1-2 theme candidates are identified, present them briefly to the user (via `AskUserQuestion`, or directly in text if the options are clear):
- Theme name + a 1-2 sentence description
- Why this theme fits the technology being learned (name the flagship features it will touch)
- An estimate of the final complexity (roughly how many milestones)

Don't proceed to Step 4 (designing the full roadmap) until this is confirmed.
