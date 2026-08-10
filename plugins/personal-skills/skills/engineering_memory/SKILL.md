---
name: engineering_memory
description: >
  Keeps a persistent, written record of decisions, experiments, regressions, and API/cost spend
  across a long-running research-and-build project, so rationale survives context compaction,
  session restarts, and handoff to another agent or person — instead of living only in the current
  conversation where it gets summarized away or lost. Trigger whenever a project spans multiple
  sessions or days (a hackathon, a multi-day feature, an ongoing research/tuning effort), after any
  iteration that changed a prompt/pipeline/architecture and produced a measurable result (better or
  worse), when the user asks "왜 이렇게 했었지", "이전에 뭘 시도했었지", "지금까지 뭐 했는지 정리해줘",
  wants to hand a project off to another agent/tool/person, needs to report cumulative API spend, or
  a bug just got fixed and should become a permanent regression case instead of a one-off patch.
  Use alongside `research_engine` (that skill decides what to try next; this one records what was
  learned so it doesn't have to be re-derived) but it's useful on its own too, any time work needs
  to survive past the current context window. Like `research_engine`, once a project has been
  identified as long-running/research-shaped this keeps applying on later terse commands ("이어서
  하자", "다음 것도 진행해") within that same project — logging shouldn't require the user to
  explicitly ask for it every time a decision gets made.
---

# Engineering Memory

## Why this exists

A long agentic session accumulates hard-won context: why an approach was rejected, what a
regression looked like last time, how much has actually been spent so far. None of that survives
context compaction reliably, and none of it is visible to a different session, a different agent
(Codex, Gemini CLI, a teammate), or an AI judge reviewing the final work. If it isn't written down
somewhere durable, it's gone the moment the conversation that produced it ends — and the next
session re-derives it from scratch, or worse, re-makes the same mistake.

This skill is the "write it down" half of the loop that `research_engine` starts. That skill's
Decision Trace and Research Memo aren't meant to stay inside a chat response — they're meant to
land in a file that outlives the conversation.

## Where to write things

Check for an existing home before creating a new one:

1. **An existing project log or decision doc** (`log.txt`, `CLAUDE.md`, `DECISION_LOG.md`,
   `CHANGELOG.md`, a `docs/` folder with a research log already in it). If one exists, append to
   it in its existing style rather than starting a competing file — a project should have one
   source of truth for "what happened and why," not several half-maintained ones.
2. **If none exists and the project looks like it'll run more than one session**, create
   `DECISION_LOG.md` and/or `RESEARCH_LOG.md` at the project root the first time you'd otherwise
   lose something worth keeping. Don't create it preemptively for a project that turns out to be
   a single quick task.
3. **A runtime decision ledger (AEL)**, if the project has one, is not a substitute for this. AEL
   records what *the system being built* decided about its inputs (e.g. why a router muted a
   specific message); this skill records what *you, building it*, decided about the system itself
   (e.g. why you added a grounding field to the prompt). If the project has both, a Research Memo
   entry can cite specific AEL query results as evidence — see `ael-ssot-debug` for how to pull
   those.

## What to log, and when

Not every message needs an entry — that would drown the signal. Log after:

- **A decision with real alternatives** — use the Decision Trace format
  (`references/decision_log_template.md`) whenever more than one reasonable approach existed and
  you picked one. Skip it for decisions that had no real alternative.
- **An experiment/iteration that produced a measurable result** — use the Research Memo format
  (`references/experiment_template.md`), including especially negative results. A reverted change
  that isn't logged will very plausibly get re-tried later by a future session that has no way of
  knowing it already failed.
- **A newly discovered bug or failure case** — becomes a permanent regression case, not just a
  patch. Use `references/regression_template.md`: what broke, the minimal input that reproduces
  it, what the fix was, and a note that this case should be checked on future changes (folded into
  an eval set/harness if one exists).
- **API/compute spend**, whenever it's non-trivial or a budget was mentioned — cumulative spend
  tracked over an entire session is easy to under-report if each run only logs its own delta (a
  real bug from the source project: a "cumulative" cost tracker that summed *current cache files*
  silently under-reported true spend by ~3-4x once repeated full re-runs overwrote earlier cache
  entries). When in doubt, sum every individual run's logged cost by hand rather than trusting a
  single running counter, and say so if you catch a discrepancy — flag it to the user before
  spending more, the way you'd flag any other risk.
- **Before a handoff** — to another agent, another session, or a person picking this up later.
  Summarize current state, open questions, and next steps in whatever log file already exists
  rather than assuming context will carry over; it won't.

## How to write an entry

Keep entries terse and evidence-grounded — a log that requires as much effort to read as the
original work isn't serving its purpose. State the decision or result, the reason grounded in
actual evidence (a metric, a specific failed case, a cost figure), and what's still open. See
`references/decision_log_template.md`, `references/experiment_template.md`, and
`references/regression_template.md` for the exact shapes — they're deliberately short.

## Signs this skill should have been used but wasn't

- You're asked "왜 이렇게 했었지" or "이전에 뭘 시도했었지" and have to reconstruct the answer by
  re-reading old messages or re-deriving it from the code, rather than reading a log.
- A fix from three sessions ago silently regressed because nothing caught it — it was never
  turned into a permanent regression case.
- Reported cumulative cost turns out to be wrong when recomputed by hand.

If any of these happen, that's the moment to start the log, not a sign it's too late to bother.
