---
name: hackathon-interview-prep
description: Prepare for a live/AI-judge post-submission interview after a hackathon agent build is functionally done (e.g. HackerRank Orchestrate). Runs a fresh-eyes evaluator subagent against ONLY the actual submission files, drills the user on explaining their own agent out loud, and preps a self-directed question with a full answer. Trigger on things like "개발 끝났으니 인터뷰 준비하자", "인터뷰 대비 시작하자", "AI judge 인터뷰 준비해줘", "이제 인터뷰 준비할까", or any request to prepare for a hackathon interview, judge Q&A, or "explain your agent" defense — even if the user doesn't name this skill directly.
---

# Hackathon Interview Prep

## Why this exists

Built after a HackerRank Orchestrate submission scored well on the built system
(chat transcript, output correctness, code quality — all "artifact quality"
categories) but noticeably worse on the live AI-judge interview. Two root
causes, diagnosed directly by the user across several turns, not guessed:

1. **Shallow self-understanding under live questioning.** The user could
   produce excellent written documentation (with help) but sometimes couldn't
   explain parts of their own agent fluently when asked live — to the point of
   needing to ask Claude for the answer *during interview prep*, which meant
   the understanding never actually transferred to the user.
2. **Technical-vocabulary production gap in spoken English** — not listening
   comprehension (explicitly ruled out by the user). The user understands
   questions and knows the answers conceptually, but lacks practiced English
   phrasing for the project's own technical vocabulary, which slows down
   live spoken answers.

A third finding: prep questions Claude generated (with full session context)
overlapped substantially with real interview questions, most likely because
the real interviewer is *also* an LLM reasoning over the submitted artifact —
not because Claude guessed well from general knowledge. That means the best
prep-question generator is a reviewer with the **same information the real
judge has, and nothing more** — not one with the whole project history.

Do not run this before the build is functionally complete — it consumes
review/practice time and needs finished submission artifacts (code.zip
contents, output.csv, README) to work from.

## The four steps

Run these roughly in order, but treat them as a menu — if the user only has
time for one, Step 2 (fresh-eyes evaluator) plus Step 3 (spoken mock Q&A) is
the highest-value combination, since it directly targets both root causes.

### Step 1 — Deep self-understanding walkthrough

Before generating any questions, walk the user through their own agent
stage by stage — architecture layers, key design decisions, what was tried
and reverted (negative results are gold here), the eval/testing methodology,
and the final metrics including the honest limitations. For each stage:

- Explain it once yourself if useful for orientation, but then **ask the
  user to explain it back in their own words** before moving to the next
  stage. Don't just hand over a finished document and assume it transfers.
- Spend real time on the "why," not just the "what" — judges probe design
  rationale ("why this approach and not X") far more than mechanics.
- This directly serves the near-universal opening question: *"Explain the
  agent you built."* Treat that question as certain to be asked and get the
  user to a point where they can answer it unprompted, start to finish,
  without notes.

### Step 2 — Fresh-eyes evaluator subagent

Spawn a subagent (Agent tool, `general-purpose` or similar) whose prompt
gives it **only** what the real AI judge would actually see — nothing else:

- The contents of the submission package (e.g. everything inside `code.zip`,
  unpacked)
- The output file (e.g. `output.csv`)
- Any README/setup docs that ship inside the package

Explicitly do **not** give it: the project's CLAUDE.md / decision log, the
chat transcript, prior eval reports, or any other session-only context. The
entire point is that it must NOT already know the backstory — a subagent
briefed with full context will generate questions Claude would ask, not
questions a naive first-time reviewer would ask, and the goal is to
approximate the latter.

Ask it to:

1. Review the material as if seeing it for the very first time.
2. List concrete questions it's curious about, grounded in specific files,
   lines, or metrics it actually observed (not generic hackathon questions).
3. Flag anything that reads as a weak point, an unexplained design choice,
   or a metric that stands out as unusually low/high compared to the rest
   (e.g. "why is this one number worse than the others?").
4. Where useful, actually try to answer/critique first, the way a skeptical
   reviewer would — this surfaces sharper follow-up questions than a flat
   question list.

Use its output as the real prep material — more so than any question list
Claude would generate directly in the main conversation.

### Step 3 — Spoken mock Q&A

Take the questions from Step 2 (plus the certain opener from Step 1) and
have the user answer them **out loud, in the interview's actual language**,
without reading from a script. The goal is producing fluent technical speech
under time pressure, not writing better answers — the user already knows the
content by this point; the gap is spoken delivery.

- Coach on vocabulary and phrasing for this project's own technical terms
  specifically (e.g. whatever the equivalents of "content-hash caching,"
  "structured output schema," "held-out test set" are for the current
  project) — drill saying each term/concept as a full spoken sentence, not
  just recognizing it when read.
- Time the answers if useful, but the target is fluency over speed for its
  own sake.
- If the user stumbles on a concept (not just the phrasing), that's a sign
  Step 1 needs more depth on that specific piece — loop back rather than
  drilling a shaky answer smooth.

### Step 4 — Prepare the self-directed question

Many of these interviews end with something like "now ask yourself a
question." Prepare this deliberately rather than improvising it live:

- Pick the project's strongest **"found and fixed/reverted a mistake"**
  story — a concrete negative result (tried X, measured it, X made things
  worse, reverted X) is one of the highest-signal things a technical
  interview can hear, because it demonstrates real empirical process rather
  than just describing a finished system.
- Alternatively, pick the metric that stands out as the weakest in the
  results (per Step 2's evaluator) and prepare it as the self-directed
  question.
- Critically: **always pair the question with the user's own full answer on
  the spot** — the question alone (e.g. "why didn't you ask me about X")
  reads as deflection; the question plus a real analysis (what caused it,
  what would have fixed it with more time/budget) reads as depth. Rehearse
  the question-plus-answer as a single unit, not two separate pieces.

## Notes for future runs

- If the hackathon has multiple interview rounds, ask the user afterward
  whether the two rounds asked overlapping questions, and update this
  process (or the user's memory) with what changed between rounds if so.
- If a recording or transcript of the interview becomes available next
  time, use it directly for feedback instead of relying on the user's
  after-the-fact recollection — recall is lossy (this skill was written
  partly because no recording existed for the run that prompted it).
- This skill is deliberately generic to "a hackathon with a live/AI-judge
  interview about a submitted agent" — it isn't tied to HackerRank
  Orchestrate specifically, so it should trigger for similarly-shaped
  interviews on other platforms too.
