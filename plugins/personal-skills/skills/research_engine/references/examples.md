# Research Engine — Worked Example

Reconstructed from an actual hackathon session (a WhatsApp message-notification router built
under a 24-hour deadline) to show the loop applied to a real accuracy-improvement task —
including a hypothesis that failed validation and was correctly reverted, not shipped anyway
because work had already been done on it.

## Context

The router classified incoming messages into `notify` / `digest` / `mute` plus a `message_type`,
with a `confidence` score. On a 30-sample gold eval it scored 86.67% action accuracy / 90%
message_type accuracy. The user had two observations from testing: (1) `digest`-gold messages
were frequently predicted `notify`, and (2) wrong predictions seemed to "feel" less confident than
right ones, without hard numbers to back that feeling up.

## 1. Restate the goal

Improve action/message_type accuracy using internal reasoning structure, without touching the
required output schema (`action, message_type, reason, confidence, evidence_message_ids` — fixed
by the problem statement) and while minimizing further API spend (explicit user constraint at
this point in the project).

## 2. Mental model

Input → per-message context assembly (user profile, group/business relationship, cached media
analysis, notification load, relevant history) → single LLM call → structured JSON output →
written to `output.csv`. The likely break point: the model reasons about sender trust, urgency,
and risk *implicitly* inside one shot, with nothing forcing it to surface that reasoning before
committing to a final action — so a wrong final answer gives no visibility into which internal
judgment went wrong.

## 3-4. Hypotheses and failure classification (done together here — the user's two observations
were validated against real data *before* any hypothesis was accepted)

Before proposing anything: pulled the actual miss list from the 30-sample + synthetic sets.
Confirmed digest→notify was the single most common miss direction (3 of 7 combined misses) —
so F6 (ambiguous label boundary between notify and digest) was real, not a guess. Confirmed wrong
predictions carried visibly lower average confidence than correct ones (0.70 vs 0.85 across 49
cases) — F4 (miscalibrated confidence) was also real, and gave a usable signal: uncertainty itself
could be used as a routing hint, not just a reported number.

| # | Hypothesis | Why it might work | Cost |
|---|---|---|---|
| H1 | Add internal-only scratch fields (sender_trust, urgency_signal, risk_signal, repetition_signal, type_candidates) filled before the final answer, never written to output.csv | Forces the model to reason explicitly before committing, giving a hook for a "default to digest when notify-vs-digest is close" rule | Small prompt/schema change, one targeted validation run |
| H2 | Add a `key_phrase` field grounding each type_candidate in actual quoted message text | Might reduce hallucinated category reasoning (F5) | Same, tested after H1 |

## 5. Bottleneck ranking

H1 targets the two *confirmed* failure modes directly (F6 + F4) — highest ROI, tried first. H2
targets a failure mode (F5) that hadn't actually been confirmed as present yet — lower priority,
tried second and only if H1 succeeds without using up the (explicitly limited) remaining budget.

## 6. Validate cheaply, then fully — this is the load-bearing step

**H1**: Reclassified only the 7 previously-wrong cases first (cheap — 7 calls, not 30 or 110).
3 of 7 flipped to correct, no new misses introduced. Only *then* spent a full 30-sample re-run to
check for regressions: 86.67%→93.33% action, 90%→93.33% message_type, no regression. Accepted.

**H2**: Same pattern — implemented, then validated on the 30-sample set (synthetic held-out set
skipped this time specifically to conserve the now-limited remaining budget, a deliberate
cost-aware tradeoff, not an oversight). Result: 93.33%→86.67% action, 93.33%→90% message_type — a
real regression, not noise. The cheap-then-full pattern caught this before it reached the 110
real messages that actually get submitted.

## 7. Decision trace

```
Decision:            Ship H1 (internal grounding fields). Do not ship H2 (key_phrase).
Reason:               H1 fixed the two confirmed failure modes with a validated, regression-free
                      improvement. H2 regressed a validated baseline on the same eval set.
Alternatives:         Leaving the single-shot reasoning as-is; the user's own key_phrase idea.
Rejected because:     Single-shot reasoning had a demonstrated blind spot (F6, F4). key_phrase
                      demonstrably regressed accuracy despite being a reasonable-sounding idea.
Risks:                Internal fields add prompt length / latency cost; acceptable given the
                      accuracy gain and no output-schema change required.
Future improvement:   If budget allows later, retest key_phrase with a larger n before concluding
                      it's a dead end outright — n=30 regression is suggestive, not certain.
```

## 8-9. Simplicity check and post-implementation validation

No simpler fix was available that addressed the *confirmed* F6/F4 issue — a prompt-only rule
without the internal fields was the simpler alternative and had already been tried in an earlier
iteration with a smaller gain, so this was a deliberate escalation, not the first thing reached
for. After shipping H1, the full 110-message production set was reclassified with the new prompt,
and cache-status/schema checks confirmed no output-format regression.

## 10-11. Self-critique and research memo

```
## Summary
Added internal grounding fields to force explicit reasoning before the final decision; this fixed
the two data-confirmed failure modes without regressing the eval set. A follow-up idea
(key_phrase grounding) was tried and reverted after it regressed the same eval set.

## Findings
digest→notify was the dominant miss direction; wrong predictions carried systematically lower
confidence than right ones. Both were verified against real miss data, not assumed.

## What improved
Action accuracy 86.67%→93.33%; message_type accuracy 90%→93.33%; no regression on synthetic set.

## What regressed
key_phrase variant: action 93.33%→86.67%, message_type 93.33%→90% — reverted, not shipped.

## Remaining failures
Evidence-selection F1 (weak evidence citation) untouched by this iteration; still open.

## Next experiment
If budget reopens, retest key_phrase on a larger n before ruling it out for good — current
n=30 result is suggestive of a real regression but not conclusive at that sample size.
```

Note what this memo makes possible: a later session (or a different agent entirely) can read this
and know *not* to re-try key_phrase without first getting more data — without that memo, the next
attempt would burn budget re-discovering the same regression from scratch.
