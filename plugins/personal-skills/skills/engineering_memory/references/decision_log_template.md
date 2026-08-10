# Decision Log — Entry Template

One entry per real decision (i.e. one where more than one reasonable option existed). Append to
the project's existing log file; don't create a second one if one already exists.

```
## [<date/time>] <short title of the decision>

Decision:            <what was chosen, one sentence>
Reason:               <why, grounded in evidence — a metric, a specific case, a cost figure,
                      not just "seemed better">
Alternatives:         <what else was considered, briefly>
Rejected because:     <the concrete reason each alternative lost, not just "worse">
Risks:                <what could still go wrong with the chosen option>
Future improvement:   <what would be worth revisiting if this stops being good enough>
```

## Example (reconstructed from a real project)

```
## [2026-08-02 14:35] Add internal grounding fields to the routing prompt

Decision:            Add sender_trust/urgency_signal/risk_signal/repetition_signal/
                      type_candidates as internal-only schema fields filled before the final
                      action/message_type/confidence, never written to output.csv.
Reason:               Confirmed against real miss data (not assumed) that digest->notify was
                      the dominant miss direction and that wrong predictions carried
                      systematically lower confidence (0.70 vs 0.85 avg) than correct ones.
                      Internal fields give the model an explicit reasoning hook to address both.
Alternatives:         Leave single-shot reasoning as-is; a simpler prompt-only disambiguation
                      rule without added schema fields (tried in an earlier iteration, smaller
                      gain).
Rejected because:     Single-shot reasoning had a demonstrated, data-confirmed blind spot on
                      exactly these two failure modes; the smaller prompt-only fix had already
                      been tried and plateaued.
Risks:                Added fields increase prompt length and per-call cost slightly.
Future improvement:   A related idea (key_phrase grounding) was tried next and reverted after
                      regressing the eval set — see Research Log entry same date, don't re-try
                      without more data first.
```
