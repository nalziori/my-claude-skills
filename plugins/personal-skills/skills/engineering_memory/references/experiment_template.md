# Research Memo — Entry Template

One entry per iteration/experiment that produced a measurable result — including, especially,
ones that ended in "reverted, no improvement." Pairs with `research_engine`'s experiment-design
and validation steps; this is where the result of that process gets written down.

```
## [<date/time>] <short title>

### Summary
<one or two sentences: what this iteration was about>

### Findings
<what the evidence showed, including negative results>

### What improved
<metric deltas, concretely, with the eval set they came from>

### What regressed
<metric deltas, concretely — "none observed" is a valid, worth-stating answer>

### Remaining failures
<what's still broken>

### Next experiment
<the next highest-ROI thing to try>
```

## Example (reconstructed from a real project, a genuine negative result)

```
## [2026-08-02 14:35] key_phrase grounding — reverted

### Summary
Tried adding a key_phrase field to ground each type_candidate in quoted message text, to test
whether it would reduce hallucinated category reasoning.

### Findings
Validated on the 30-sample eval set only (synthetic held-out set deliberately skipped to
conserve a now-limited remaining budget — a cost-aware tradeoff, not an oversight).

### What improved
Nothing — see regression below.

### What regressed
Action accuracy 93.33% -> 86.67%; message_type accuracy 93.33% -> 90%, both against the same
eval set the prior (accepted) iteration had improved. Reverted immediately; the prior iteration's
prompt was restored and the full 110-message production set was reclassified with it.

### Remaining failures
Evidence-selection quality (weak evidence citation) is still an open, untouched failure mode.

### Next experiment
If budget reopens, retest key_phrase on a larger n before ruling it out for good — n=30 is
suggestive of a real regression but not conclusive at that sample size. Don't re-attempt without
more data; the first attempt is now on record.
```

## Why the negative result matters as much as the positive one

The entry above is what stops a future session (or a different agent picking up the project) from
burning API budget re-discovering the same regression from scratch. A memo that only records wins
is missing the half that actually saves the most time later.
