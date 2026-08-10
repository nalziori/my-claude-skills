# Regression Case — Entry Template

Every newly discovered bug or failure case becomes a permanent case, not just a silent patch. If
the project has an eval harness or test suite, fold the case into it; if not, keep the entries in
this log so a future change can be checked against them by hand.

```
## [<date/time>] <short title of what broke>

What broke:          <symptom, concretely>
Minimal repro:        <the smallest input/state that reproduces it>
Root cause:            <why it actually happened — not just what the symptom was>
Fix:                   <what changed>
Check going forward:  <what a future change should verify to avoid re-breaking this>
```

## Example (reconstructed from a real project)

```
## [2026-08-02 12:57] validate command overcounted message rows

What broke:          `validate` reported 264 rows for messages.csv when the actual row count
                      was 110.
Minimal repro:        Any row in messages.csv containing an embedded newline inside
                      message_text (a naive line-count treats each embedded newline as a new
                      row).
Root cause:            Row counting used a plain line-count instead of a CSV-aware reader, so
                      multi-line quoted fields were miscounted.
Fix:                   Switched to csv.reader for the count instead of counting raw lines.
Check going forward:  Any future change to file-counting/validation logic should be tested
                      against a CSV file with at least one embedded-newline field, not just a
                      simple single-line-per-row file.
```

## Example (a structural cost-tracking bug, same project)

```
## [2026-08-02 14:35] Cumulative cost tracker under-reported real spend

What broke:          `cache-status`'s cumulative cost figure reported ~$2 when hand-summing
                      every individual run's logged cost showed true spend was closer to
                      $5.7-6.9.
Minimal repro:        Run a full reclassification (`route --force`) more than once — each run
                      overwrites the same cache files, and the "cumulative" figure summed
                      *current* cache files rather than accumulating cost across every run
                      that had actually happened.
Root cause:            The cumulative tracker was structurally wrong for any workflow with
                      repeated full re-runs over the same cache keys, not just a display bug.
Fix:                   Manually recomputed true cumulative spend from every individual "cost
                      this run" figure logged so far; reported the discrepancy to the user
                      transparently before any further spending.
Check going forward:  Don't trust a single running cost counter in a project with repeatable
                      full re-runs — verify against the sum of individual run logs periodically,
                      especially before reporting remaining budget to the user.
```
