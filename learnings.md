# Learnings — Signal Digest

## What I built and why it matters

This project is my first working AI agent. It monitors 7 RSS sources, reasons over the content through my professional lens, and delivers a curated weekly digest to my inbox every Monday. But more importantly, building it taught me the difference between a script and an agent — and where the intelligence actually lives.

---

## Script vs Agent — The Core Distinction

Most "AI projects" people build are actually just scripts with an LLM call at the end. The distinction matters because it changes how you think about what you're building.

### A script is deterministic

```
INPUT → STEP 1 → STEP 2 → STEP 3 → OUTPUT
```

Every run follows the same path. The logic is hardcoded. There's no judgment — only execution. A script that summarizes articles would:

```
fetch articles → summarize each one → email summaries
```

It doesn't decide what matters. It processes everything equally. You get output, but not intelligence.

### An agent reasons and decides

```
INPUT → [PERCEIVE → REASON → ACT → OBSERVE] → OUTPUT
            ^___________________________|
                     the loop
```

An agent doesn't just process — it makes judgment calls. It can decide to skip something, prioritize something else, cluster related ideas, and stop when it's done. The loop is the key: it observes the result of its actions and can adjust.

---

## How this project maps to that distinction

```
┌─────────────────────────────────────────────────────────────┐
│                      SCHEDULER                              │
│                 Windows Task Scheduler                      │
│            Runs run_tracker.bat every Monday 10 AM          │
│                                                             │
│                  NOT the agent.                             │
│                  Just a trigger.                            │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                       FETCHER                               │
│                    fetcher.py                               │
│                                                             │
│  - Loops through 7 RSS sources                              │
│  - Parses each feed with feedparser                         │
│  - Filters articles older than 7 days                       │
│  - Returns a flat list of article dicts                     │
│                                                             │
│                  NOT the agent.                             │
│                  Just data collection.                      │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │  ~37 raw articles
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ████████████████████████████████████████████████████████  │
│  █                                                        █ │
│  █                   THE AGENT                            █ │
│  █                   agent.py                             █ │
│  █                                                        █ │
│  █  PERCEIVE  →  reads all 37 articles                    █ │
│  █                                                        █ │
│  █  REASON    →  is this relevant to Job's lens?          █ │
│  █             →  agentic AI? RevOps? AI PM thinking?     █ │
│  █             →  would this shift his thinking?          █ │
│  █                                                        █ │
│  █  DECIDE    →  keep or discard (ruthless filter)        █ │
│  █                                                        █ │
│  █  ACT       →  extract signal (not summary)             █ │
│  █             →  cluster related signals by theme        █ │
│  █             →  write digest in Job's context           █ │
│  █             →  pick signal of the week                 █ │
│  █                                                        █ │
│  █  OBSERVE   →  is the digest complete and coherent?     █ │
│  █             →  yes → stop and return output            █ │
│  █                                                        █ │
│  ████████████████████████████████████████████████████████  │
│                                                             │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │  curated digest (markdown)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      DELIVERY                               │
│                    deliver.py                               │
│                                                             │
│  - Converts markdown → HTML (mobile-friendly)              │
│  - Saves digest to archive/ as dated .md file              │
│  - Sends HTML email via Gmail SMTP                          │
│                                                             │
│                  NOT the agent.                             │
│                  Just output transport.                     │
└─────────────────────────────────────────────────────────────┘
```

---

## What makes the agent the agent

The agent is not the whole pipeline. It's specifically the reasoning loop in `agent.py`.

Three things make it an agent and not a script:

**1. It makes judgment calls**
A script summarizes everything. The agent decides what's worth including. 37 articles in, ~8 signals out. That filtering is judgment, not logic.

**2. It reasons about a specific person**
The system prompt gives Claude a persona — Job's lens, Job's goals, Job's context. The agent doesn't just extract information, it reasons about *relevance to a specific reader*. That's a form of goal-directed behavior.

**3. It decides when it's done**
A script runs all its steps and stops. The agent produces output when it's satisfied the task is complete — when the digest is coherent, clustered, and includes a signal of the week. It self-evaluates before returning.

---

## What I learned about agent design

### Tools are what give agents reach
An agent without tools is just a chatbot. Tools are how an agent affects the world — in this project, `feedparser` (read the web) and `smtplib` (send email) are the tools. The LLM reasons; the tools act.

### The system prompt is the agent's identity
The most important engineering decision in this project wasn't the code — it was the system prompt in `agent.py`. It defines:
- Who the agent is reasoning for
- What counts as signal vs noise
- How the output should be structured
- The tone and voice of the digest

A bad system prompt produces a generic summarizer. A good one produces a personal analyst.

### Plumbing is not intelligence
The scheduler, fetcher, and delivery modules are all plumbing. They're necessary but not interesting. The intelligence lives entirely in the agent loop. This is a useful mental model for evaluating any "AI project" — ask where the judgment is. If there's no judgment, it's a script.

### Hallucination is a real agent risk
During the first run, the agent produced references to articles (Project Glasswing, GLM-5.1) that may not have been in the fetched RSS content — it drew on its own training knowledge to fill gaps. This is a known agent failure mode: the model reasons beyond the data it was given. Future fix: tighten the system prompt to explicitly instruct the agent to reason only over the provided articles.

---

## What I built next

**Deduplication** ✓ — `cache.json` stores seen article URLs between runs. The fetcher loads the cache at startup and skips any URL already seen, then saves the new batch before returning. Corrupt cache falls back gracefully to an empty set.

**Error handling** ✓ — Each RSS source is now wrapped in try/except. `feed.bozo` catches silent feedparser failures (network errors don't raise exceptions — they return a malformed feed object). The agent and email send are also guarded independently so one failure doesn't cascade. `main.py` exits with code 0/1 so schedulers can detect failures.

**Hallucination guard** ✓ — The system prompt now includes a CRITICAL CONSTRAINTS block that explicitly instructs Claude to reason only from the provided articles, skip anything too vague to assess, and not draw on training knowledge. The user message reinforces it. Cross-article synthesis (spotting a trend across two articles) is still permitted — the constraint is against training knowledge, not synthesis.

**HTML rendering** ✓ — Replaced the custom line-by-line regex converter with the `markdown` library (`extra` + `nl2br` extensions). Handles nested markdown, tables, code blocks, and blockquotes correctly — things the regex approach silently broke.

**Source expansion** ✓ — Added 5 feeds: LangChain Blog, Hugging Face Blog (Agentic AI), Andrew Chen (AI PM), OpenView Partners (RevOps), GitHub Changelog (Builder mindset). The agent's system prompt naturally filters new sources through Job's lens — no prompt changes needed.

**Cross-platform scheduler** ✓ — Added `scheduler/` with cron, launchd (macOS), and systemd configs so the pipeline isn't tied to Windows Task Scheduler.

---

## What's still worth building

**Memory** — store the agent's previous digests and let it notice patterns over time. "This is the third week Simon Willison has written about on-device AI — this is now a trend, not a signal."

**MCP integration** — when this project grows to use multiple tools across multiple agents, MCP (Model Context Protocol) would let tools be standardized and reusable rather than custom-wired per project.

---

## One-line summary

> A script executes steps. An agent makes decisions. The difference is judgment — and judgment lives in the loop.
