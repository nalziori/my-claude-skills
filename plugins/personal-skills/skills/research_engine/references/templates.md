# Research Engine — Templates

Copy the relevant block, fill it in inline in your response or in a scratch file. These aren't a
rigid schema to satisfy — they're a shape that's proven useful for making sure nothing gets skipped.

## Hypothesis table

| # | Hypothesis | Why it might work | Expected improvement | Possible regression | Impl. cost | Eval cost |
|---|---|---|---|---|---|---|
| H1 | | | | | | |
| H2 | | | | | | |
| H3 | | | | | | |

Aim for 3-5. If you can only think of one, you probably haven't looked at enough failing cases yet.

## Failure taxonomy (starter categories — rename/extend for the domain)

| Code | Category | Example signal |
|---|---|---|
| F1 | Missing context | The system never had the information it needed to decide correctly |
| F2 | Weak retrieval | Relevant evidence existed but wasn't surfaced |
| F3 | Prompt underspecifies an edge case | Two similar-looking inputs need different handling and the prompt doesn't say so |
| F4 | Miscalibrated confidence | Wrong answers carry similar or higher confidence than right ones |
| F5 | Hallucinated evidence | Cited evidence doesn't actually support the conclusion |
| F6 | Ambiguous label/category boundary | Reasonable people (or gold labels) would disagree on the right bucket |
| F7 | Concurrency / infra bug | Wrong output for a reason unrelated to the model's reasoning at all |

Tag every miss with a code before proposing a fix. If most misses share a code, that's the
highest-ROI bottleneck — see the ranking step.

## Experiment plan

```
Hypothesis:        <what you're testing>
Expected outcome:   <what "it worked" looks like, concretely, in numbers if possible>
Failure condition:  <what "it didn't work" or "it regressed" looks like>
Evaluation set:     <cheap targeted subset first, then the full/held-out set>
Metrics:            <what you're measuring>
API cost estimate:  <rough $ or call count, if relevant>
```

## Decision trace

```
Decision:            <what was chosen>
Reason:               <why, grounded in evidence from the experiment above>
Alternatives:         <what else was considered>
Rejected because:     <why each alternative lost>
Risks:                 <what could still go wrong>
Future improvement:    <what would be worth trying if this stops being good enough>
```

## Research memo (end of iteration)

```
## Summary
<one or two sentences: what this iteration was about>

## Findings
<what the evidence showed, including negative results>

## What improved
<metric deltas, concretely>

## What regressed
<metric deltas, concretely — "none observed" is a valid, worth-stating answer>

## Remaining failures
<what's still broken, tagged with a failure-taxonomy code if possible>

## Next experiment
<the next highest-ROI thing to try, per the bottleneck ranking>
```

## Self-critique prompts (ask yourself before closing an iteration)

- What assumptions did I make that I never actually verified?
- Is the sample size big enough that this result isn't noise?
- What evidence, if I looked for it, might contradict my own conclusion?
- If I only tested the cases that motivated this fix, would it survive being re-tested on cases
  that didn't?
