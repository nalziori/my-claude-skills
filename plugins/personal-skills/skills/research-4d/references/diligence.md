# Diligence checklists

Diligence is continuous. Run the relevant section when you reach the stage it applies to; run the
final validation before declaring the project complete.

A standing limit applies to everything here: **you do not issue legal or ethical clearance.** You
identify concerns, explain why they matter, and route them to the institution, the IRB, the data
owner, or a qualified reviewer. "This looks fine legally" is not a sentence you write.

---

## Data ethics and legality — check before collecting (stage 2)

- [ ] Was the collection method ethical?
- [ ] Was it legal in the relevant jurisdiction?
- [ ] Do the source's terms of use permit research use, and permit this specific use?
- [ ] Is the licensing compatible with how the results will be published?
- [ ] For scraped or social media data: does use infringe copyright or the platform's terms?
- [ ] Did subjects consent, where consent is required?
- [ ] Is there a data use agreement, and does this analysis stay inside it?

Scraping and social-media corpora are where this most often goes wrong, because collection is
technically easy and the terms are rarely read. Check before, not after.

## Personal information

- [ ] Does the dataset contain direct identifiers (name, ID number, contact, precise location)?
- [ ] Does it contain quasi-identifiers that re-identify in combination (birth date + ZIP + sex is
      the classic example)?
- [ ] Has de-identification or pseudonymization actually been applied before modeling?
- [ ] Is the key, if any, stored separately with restricted access?
- [ ] Will any output — a figure, a table, a small subgroup count — leak an individual?
- [ ] Is the retention period defined?

De-identification is a step that gets planned and then skipped under deadline. Verify it ran.

## Human-subjects research

Applies to medical, behavioral, biometric, educational, or any individual-level human data.

- [ ] Is IRB or ethics committee approval required?
- [ ] Does existing approval cover *this* analysis, including the AI-assisted pipeline?
- [ ] Are secondary-use restrictions on the dataset respected?
- [ ] Are vulnerable populations involved, and are the extra protections in place?

If any of these is unclear, stop and route to the institution. Do not proceed on the assumption
that it is probably fine.

## Sampling bias — check during EDA (stage 4)

Examine representation across the demographic variables the research actually requires — typically
some of sex, age, geography, race or ethnicity, socioeconomic status, language.

- [ ] Is the sample distribution documented and compared against the target population?
- [ ] Is any group systematically under- or over-represented?
- [ ] Is missingness itself patterned by group? (Differential missingness is bias that survives
      imputation.)
- [ ] Are selection effects in how the data was collected documented?
- [ ] Is the resulting limit on generalizability stated in the write-up?

Only collect and analyze demographic variables the research genuinely needs. Fishing for
subgroup effects is its own ethical problem.

## Fairness — for predictive and classification models

- [ ] Could the model's output disadvantage a group?
- [ ] Is performance disaggregated by group, not just reported in aggregate?
- [ ] Is an appropriate fairness metric chosen and justified for this context?
- [ ] Are proxy variables for protected attributes identified?
- [ ] Is the deployment context considered, or is this research-only?

Fairness metrics conflict mathematically — you cannot satisfy all of them at once. Choose one that
matches the actual harm you are trying to prevent, and state why.

## Causal language discipline

Keep these distinct in every sentence you write and every sentence you review:

| Term | Warranted when |
|---|---|
| **correlation** | Two variables covary. Nothing more. |
| **association** | A relationship holds, possibly adjusted for covariates. Still not causal. |
| **prediction** | The model forecasts the outcome. Says nothing about mechanism. |
| **causal effect** | Only with an experimental design, or a credible identification strategy with its assumptions stated and tested. |

Verbs leak causation: *causes, drives, leads to, increases, reduces, improves, results in*. On an
observational design, use *is associated with*, *predicts*, *covaries with*. When the researcher's
draft crosses this line, correct it and show the sentence.

## Explainability

- [ ] Does this use case require explanation, or is predictive accuracy sufficient?
- [ ] If a model informs decisions about people, is SHAP, LIME, or an equivalent applied?
- [ ] Are feature importances reported with their known caveats (correlated features distort
      importance rankings)?
- [ ] Is a simpler, inherently interpretable model competitive? If so, prefer it.

## Hallucination control

Whenever an LLM summarized data, described results, or wrote a numerical claim:

- [ ] Every number in the prose traced back to the actual analysis output
- [ ] Every citation verified to exist and to say what it is claimed to say
- [ ] Every dataset description checked against the real schema
- [ ] No statistic quoted that was not computed
- [ ] Summary claims spot-checked against the raw data

This is rung 4 of the verification ladder and it is not optional for generated prose. A fabricated
summary statistic reads exactly like a real one.

## Reproducibility inputs

Capture at the moment of the decision, not at the end:

- [ ] Random seeds, everywhere randomness enters
- [ ] Library versions (a lockfile, not a list)
- [ ] Data version identifier
- [ ] Hyperparameters and their search space
- [ ] Preprocessing pipeline as code
- [ ] Hardware, where results depend on it (GPU nondeterminism)
- [ ] Evaluation harness version

## AI use disclosure

Draft this during stage 6 for the methodology or acknowledgements section:

```
AI systems used:      model name and version
Purpose:              what it was used for
Stages involved:      which of the six stages
Code generation:      yes/no, and what fraction was reviewed by the researcher
Data processing:      yes/no, and which transformations
Analysis support:     scope
Text generation:      yes/no, and which sections
Human verification:   how outputs were checked
```

Two rules that follow from this and are not negotiable:

**AI is not an author.** Authorship requires accountability for the work, and an AI cannot be held
legally or ethically responsible. Most journals now state this explicitly; follow the target
venue's policy, which will be at least this strict.

**Responsibility is the researcher's.** Every number, claim, and conclusion in the published work
is theirs, regardless of which parts an AI produced. Say this plainly when the human seems to be
treating an AI output as pre-validated.

---

## Final validation harness

Run before declaring completion. Score each criterion and record evidence.

| Criterion | What it checks |
|---|---|
| Research question alignment | The analysis actually answers the question asked |
| Hypothesis alignment | The tests performed test the stated hypothesis |
| Data integrity | Source, license, and collection are documented and legitimate |
| Data versioning | The exact data used is identifiable and retrievable |
| Preprocessing integrity | The pipeline is code, is documented, and is leakage-free |
| Statistical validity | Assumptions checked; tests appropriate; multiple comparisons handled |
| Model validity | Baseline compared; overfitting assessed; validation scheme sound |
| Evaluation integrity | Metrics appropriate; test set used once; harness passing |
| Interpretation validity | Claims match evidence; causal language correct; uncertainty stated |
| Reproducibility | A clean-state rerun reproduces the reported results |
| Ethical compliance | Ethics, privacy, licensing, and bias reviews complete |
| AI usage transparency | Disclosure drafted; authorship policy respected |

Record each as:

```
Criterion:
Expected:
Observed:
Status:    PASS | FAIL | N/A
Evidence:  file, number, or check that demonstrates it
Risk:      what remains uncertain
Action:    required fix, if FAIL
```

Any `FAIL` gets reported to the human with the specific problem and a proposed fix. Do not quietly
downgrade a FAIL to a caveat in the limitations section. If the human decides to accept a FAIL,
record that decision and its rationale in the ledger — an accepted, documented limitation is
legitimate research practice; an undocumented one is not.
