---
name: research_engine
description: >
  A research-first thinking protocol to load before starting any non-trivial build, debug, or
  improvement task on an AI pipeline or agent — restate the goal and constraints, build a mental
  model of the current system, generate 3-5 competing hypotheses, classify failures by root cause
  (not just "accuracy is low"), validate cheaply before running a full/expensive evaluation, and
  leave a decision trace instead of jumping straight to code. Trigger whenever the user wants to
  improve an AI system's accuracy or quality, debug why an agent/model is getting something wrong,
  design an evaluation or experiment, choose between several implementation approaches, or kicks
  off a multi-day/hackathon-style research-and-build project — even if they don't use research
  language explicitly, e.g. "정확도 좀 높여보자", "왜 이 케이스가 틀렸는지 봐줘", "이 프롬프트 개선 방향
  제안해줘", "새 파이프라인 설계해줘", "실험 하나 해보고 싶은데", "이거 성능이 왜 이래", "A안이랑 B안 중에
  뭐가 나을까". Critically, this also covers short follow-up commands inside a project that has
  already been established as research-shaped — "바로 진행하자", "이어서 하자", "좋아 계속해", "그렇게
  해줘" — the user should not have to re-explain research intent on every turn once a project is
  underway; treat the whole project as in scope, not just the message that first mentioned it.
  Skip this for trivial, single-step, deterministic requests (typo fix, rename, a one-line config
  change, "add a print statement") — there's nothing to hypothesize about there.
---

# Research Engine

## Why this exists

Left to its own devices, an agent under pressure (a deadline, a frustrated user, a long todo list)
converges on the first fix that could plausibly work and ships it. That produces code that runs,
but not necessarily the *right* code — and worse, it leaves no trace of what else was considered
or why the chosen approach won. Six months later nobody, including you, can tell whether a design
choice was deliberate or accidental.

This skill is not about writing better prose in your reasoning. It's a discipline: for any request
that has more than one plausible answer, generate the alternatives on purpose, rule most of them
out with cheap evidence, and only then write the expensive code or run the expensive evaluation.
Optimize for **decision quality**, not implementation speed. You are simultaneously acting as
researcher, system architect, evaluation engineer, and failure analyst — writing code is the last
of those four hats, not the first.

Pair this with [[engineering_memory]] — this skill decides *what to do next*; that one records
*what was learned* so the next session (or a teammate, or an AI-judge reviewer) doesn't have to
re-derive it. If the target project already has its own runtime decision ledger (tables like
`ael_planning`/`ael_execution`/...), that's a different layer — see the note at the bottom.

## When to apply it, and how hard

Not every request needs the full loop. Scale the rigor to the ambiguity:

- **Full loop** — the request is "make X better", "figure out why X is wrong", "design Y", or the
  first request in a new research/hackathon-style project. There's a real decision to make.
- **Light touch** — restate the goal and name 2-3 alternatives inline, then proceed. Used for
  requests where one approach is clearly best but a slightly-too-fast agent might miss an edge
  case (e.g., "add a retry to this API call" — worth a beat on backoff strategy, not a full
  experiment table).
- **Skip entirely** — deterministic, single-outcome tasks. There is nothing to hypothesize about
  in a typo fix.

If unsure which bucket a request falls into, err toward the full loop for the *first*
substantial task in a session and light touch after that, once the mental model is established.

**This persists across turns.** Once a project has been identified as research-shaped, don't wait
for the user to re-invoke research language on every message. A terse "바로 진행하자" or "다음 단계
가자" partway through such a project is a continuation of the same loop, not a new trivial request
— the goal was to let the user give short commands and still get hypothesis-driven, evidence-
checked work back, not to make them re-justify the process every time.

## The loop

### 1. Restate the goal

Rewrite the request in your own words: objective, constraints, success criteria. If any of these
are actually unclear — not just unstated but genuinely ambiguous — ask before implementing. Most
"the AI did the wrong thing" failures trace back to skipping this step, not to a bad hypothesis
later on.

### 2. Build a mental model

Before touching anything, be able to state: what goes in, what processing happens, what comes out,
what feedback signal exists (an eval score, user correction, a log), and where in that chain
things are most likely to break. If you can't answer "where would this break" yet, you don't have
a mental model — read more code/data first.

### 3. Generate hypotheses (3-5, not 1)

Never implement the first idea that comes to mind. For each hypothesis, briefly note:

- why it might work
- expected improvement
- possible regression it could introduce
- rough implementation cost
- rough evaluation cost (API calls, time)

Use `references/templates.md` for the table format. The point isn't ceremony — it's that the
second and third hypotheses you'd otherwise never write down are often better than the first.

### 4. Classify failures by root cause

Never describe a problem as "accuracy is low" or "it's not working well." Name *why*. Build a
small failure taxonomy for the current problem (missing context, weak retrieval, ambiguous label
boundary, miscalibrated confidence, prompt underspecifies an edge case, etc. — see
`references/templates.md` for a starter list). A vague failure description leads to a vague fix
that regresses something else; a named root cause leads to a fix that targets it.

### 5. Rank bottlenecks by ROI

Not every failure category is worth fixing now. For each, estimate expected improvement, cost,
and risk of regression, and prioritize the highest-ROI one. Resist fixing the most *visible*
failure if it isn't the highest-ROI one.

### 6. Validate cheaply before validating fully

Before spending a full evaluation run (or real API budget) on a change, test it against the
*specific* cases it's meant to fix. Only after that looks promising do you re-run the full/held-out
evaluation to check for regressions. This two-step pattern — cheap targeted check, then expensive
full check — is the single highest-leverage habit in this whole loop: it catches bad ideas before
they cost anything, and catches regressions before they ship. (Concrete worked example, including
a case where the full check caught a regression the targeted check missed, in
`references/examples.md`.)

### 7. Leave a decision trace

Every real architectural or prompt decision should be recoverable later: what was decided, why,
what alternatives were rejected and why, what risk remains. Don't rely on this staying in your own
context — write it down. This is exactly what `engineering_memory`'s Decision Log is for; use that
skill's template rather than inventing your own format each time.

### 8. Before implementing, ask if there's a smaller answer

Is there a simpler, cheaper, more general, or more explainable solution than the one you're about
to build? Prefer pipeline/retrieval/context improvements over prompt patching where possible —
prompt-only fixes tend to be narrow and don't generalize past the cases that motivated them.

### 9. Validate after, not just "it works"

After implementing, check regression on previously-passing cases, not just whether the new case
now passes. "It works" on the one case you were staring at is not validation.

### 10. Self-critique

After a non-trivial change, ask: what assumptions did I make? Which of those are actually
unsupported? Is there evidence that contradicts my own conclusion? If a fix "worked" on a small
sample, could that be noise (n too small) rather than a real improvement? Log.txt's own hackathon
project has a real example of this: an 86.67%→93.33% jump on n=30 was treated as signal, but a
same-magnitude single-case shift on the same n was explicitly logged as "read as noise, not a
regression" rather than chased.

### 11. Close the loop with a Research Memo

Every iteration — especially ones that end in "reverted, no improvement" — gets a short Research
Memo: what was tried, what improved, what regressed, what's still unresolved, what's next. A
negative result that gets written down is worth more than a positive result that doesn't, because
it stops the next session (or the next agent) from re-trying the same dead end. Template and a
real worked example (including a genuine negative result) in `references/`.

## Reference files

- `references/templates.md` — blank copy-paste formats for the hypothesis table, failure
  taxonomy, experiment plan, decision trace, and research memo used above.
- `references/examples.md` — a real end-to-end worked example reconstructed from an actual
  hackathon project's session log, showing the loop applied to an accuracy-improvement task,
  including one hypothesis that failed validation and was reverted.

## Relationship to a runtime decision ledger (AEL)

If the project you're working in has (or should have) its own append-only ledger recording the
*target system's* decisions — e.g. why a message router classified a specific message a certain
way — that's a different concern, covered by the `ael-ledger-setup` / `ael-ssot-debug` skills.
This skill governs how *you*, the building/researching agent, think and decide; AEL governs how
*the system you're building* explains its own runtime output. They compose: your Research Memo can
cite AEL query results as evidence, but it doesn't replace them, and setting up AEL doesn't replace
following this loop while you build.
