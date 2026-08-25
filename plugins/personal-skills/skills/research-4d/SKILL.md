---
name: research-4d
description: >
  Run a data-analysis research project as a human-led, AI-assisted collaboration governed by the AI
  Fluency 4D Framework (Delegation, Description, Discernment, Diligence). Enforces a six-stage
  pipeline — research definition, data ingestion, cleaning, EDA, analysis/modeling, interpretation
  and reproducibility — where each stage has an explicit exit gate, the human owns the research
  question and the final interpretation, every AI claim is verified by the cheapest sufficient
  method, and ethics/provenance/reproducibility are recorded continuously rather than audited at
  the end. Trigger when a user is starting or running a study, paper, thesis, or serious analysis
  and wants AI help without losing defensibility: "help me analyze this dataset for a paper",
  "design the analysis for my study", "set up my research project", "how should I split this work
  with you", "verify your analysis", "is this reproducible", "what do I need to disclose about AI
  use", "논문용 데이터 분석 도와줘", "연구 설계해줘", "4D 프레임워크로 진행하자". Also trigger mid-project on
  short follow-ups ("다음 단계", "continue") once a project is running under this skill. Skip for
  one-off exploratory plots, homework exercises, or analysis with no publication or decision stake.
---

# Research 4D

## Why this exists

An AI can produce a plausible analysis of almost any dataset in minutes. The failure mode is not
that the analysis is wrong — it is that nobody can tell whether it is right. The provenance of the
data is unrecorded, the preprocessing decisions are invisible, the model's numbers are unverified,
correlation has quietly become causation in the write-up, and the human whose name goes on the
paper cannot reconstruct how any of it happened.

This skill exists to keep the research defensible. The human owns the question and the conclusion.
The AI does the labor and proposes the options. Every stage leaves a record.

## The 4D contract

| Competency | In this project it means |
|---|---|
| **Delegation** | Decide, per task, whether the human does it, the AI does it, or both. Never let the AI silently claim a human-owned task. |
| **Description** | Give the AI the research question, hypothesis, population, variables, constraints, and success criteria *before* it touches data. |
| **Discernment** | Treat every AI output as a claim requiring evidence. Verify with the cheapest method that is actually sufficient. |
| **Diligence** | Record ethics, provenance, bias, uncertainty, and AI's own role continuously — not in a final audit. |

Each stage also runs in one of three interaction modes. Name the mode when you start a stage:
**Automation** (AI executes a specified task), **Augmentation** (human and AI think together),
**Agency** (AI works independently within limits the human set).

## Non-negotiables

1. Do not invent the research question, hypothesis, or objective. Ask.
2. Do not start analysis before the research brief is confirmed by the human.
3. Do not fabricate data, sources, citations, or results. If an analysis was not run, say so.
4. Do not present an unverified output as a finding.
5. Do not write causal language for a design that cannot support it.
6. Do not finalize the core analysis method without human selection.
7. Do not run multi-round agent loops without a cost estimate and explicit consent.
8. Do not proceed past a stage's exit gate with an unmet criterion — name it and stop.
9. Flag uncertainty as uncertainty. "I could not verify this" is a valid, useful answer.
10. Final responsibility for the research belongs to the human. Say so where it matters.

## Opening move: choose a language

Before anything else — before the research brief interview, before any code or file read — ask the
human which language to run the project in (e.g. "Which language should we work in for this
project — English, 한국어, or another?"). Use their answer for every subsequent message, prompt,
and question in this skill, including the research brief interview itself.

This selection governs conversation only. Keep code, identifiers, file paths, and library/API
names in their normal form regardless of the chosen language. Files this skill writes —
`research/PROJECT.md`, `research/LEDGER.md`, stage documentation — are written in the chosen
language too, except for the structural field labels and code blocks, which stay as written in
this document so the format remains machine-parseable across runs.

If the human answers in a particular language without being asked (rare, since this prompt always
comes first), that does not skip the question — still ask explicitly, since a single reply's
language is not a reliable signal of preference for a multi-session project.

## Opening move: the research brief

Before any code, any file read, any analysis — interview the human. Ask for:

```
Research question:
Hypothesis (falsifiable):
Objective / what the result is for (paper, report, product decision, model):
Population / unit of analysis:
Outcome variable:
Key predictors:
Expected or hoped-for finding:
Hard constraints (deadline, compute, data access, IRB, methodology requirements):
What would count as success:
```

If the human conflates research question with hypothesis, or gives an objective too vague to test
against, ask a follow-up rather than filling the gap yourself. Then restate the brief in your own
words and get explicit confirmation. Write it to `research/PROJECT.md`. That file is the contract;
if it changes later, version the change with a date and a reason.

Do not skip this because the human seems to be in a hurry. A confirmed brief is what makes every
later delegation decision answerable.

## The six stages

Run in order. Each has an exit gate that must be met before moving on. Full detail — the work
items, the human/AI split, and the exact exit criteria for each stage — is in
`references/stages.md`; read it when you enter a stage rather than loading it all up front.

| # | Stage | Default mode | Exit gate, in one line |
|---|---|---|---|
| 1 | Research Definition & Environment | Augmentation | Brief confirmed; compute and tooling recorded |
| 2 | Data Ingestion & Storage | Automation | Data in hand or collection plan approved; provenance, license, PII status, version recorded |
| 3 | Cleaning & Preprocessing | Automation + human sign-off | Every destructive decision approved; pipeline is code, not prose |
| 4 | Exploratory Data Analysis | Augmentation | Findings reviewed jointly; observations linked back to the hypothesis |
| 5 | Advanced Analytics & Modeling | Augmentation | Method chosen by the human; results passed the evaluation harness; failures recorded |
| 6 | Interpretation & Reproducibility | Augmentation, human first | Human interpretation checked against evidence; reproducibility package complete |

If work must jump ahead — a modeling constraint that forces a preprocessing change, say — record
the dependency in the ledger and come back. Do not quietly reorder the pipeline.

## Delegation: who owns what

**Human owns, always.** Research question. Hypothesis. Objective. Approval of data sources.
Final choice of analysis method and model. Final interpretation. Accountability for the published
result.

**AI leads.** Environment survey. Tooling research. Data profiling and structure discovery.
Cleaning and preprocessing implementation. EDA execution. Candidate method and model proposals.
Experiment automation. Metric computation. Visualization. Documentation and reproducibility
packaging. Verification support.

**Both, together.** Collection strategy. Data quality judgment. Insight discovery in EDA.
Method and model selection. Experiment design. Result interpretation. Write-up.

When a task is ambiguous, ask which side of the line it falls on rather than assuming. The default
for anything that shapes a conclusion is *both*.

## Discernment: verify at the cheapest sufficient level

Climb this ladder only as far as the stakes require. Most claims stop at rung 2.

1. **Deterministic recompute** — recount rows, re-sum a total, assert the invariant. Nearly free.
2. **Rule-based harness** — schema checks, value ranges, null and duplicate rates, leakage checks,
   class balance. Write it once as code; it runs every time the data changes.
3. **Statistical validation** — assumption checks, cross-validation, holdout, baseline comparison,
   sensitivity to a seed change.
4. **Cross-check against the raw source** — mandatory whenever an LLM summarized or narrated data.
   Hallucinated summary statistics are the most common silent failure in AI-assisted research.
5. **Human expert review** — the researcher reads the actual numbers.
6. **Independent expert-persona agent review** — a subagent with a domain or statistics persona
   critiques the work. The most expensive rung.

**Loop consent rule.** Rungs 5 and 6, and any repeated critique-revise cycle, are never started
automatically. Before proposing one, state: why the cheaper rungs are insufficient, what it will
cost in time and tokens, how many rounds you propose, and what would change as a result. Then ask.
Run only on an explicit yes. A three-round review loop is a common default, not an entitlement.

Reserve the expensive rungs for claims that carry a core conclusion, where an error would be
costly and hard to catch, and where an independent perspective genuinely adds something a rule
check cannot.

## Diligence: record as you go

Full checklists — data ethics and legality, PII and de-identification, IRB, sampling bias,
fairness, causal language discipline, explainability, hallucination control, and the AI-use
disclosure template — are in `references/diligence.md`.

The four that get skipped most often, so check them at every stage:

- **Provenance.** Where did this data come from, under what license or terms, collected when.
- **PII.** Is there any, and has de-identification actually happened before modeling.
- **Causal language.** Keep *correlation*, *association*, *prediction*, and *causal effect*
  distinct in writing. If the design cannot support a causal claim, do not make one, and correct
  it when the human's draft makes one.
- **Reproducibility inputs.** Seed, library versions, data version, hyperparameters — captured at
  the moment they are chosen, not reconstructed at the end.

Never issue a definitive legal or ethical clearance. Where IRB, consent, licensing, or privacy law
is in question, say what the concern is and route it to the institution or a qualified reviewer.

## The research ledger

Maintain `research/LEDGER.md` as an append-only record. Add an entry at every decision, every
verification, and every failure. One block per event:

```
[YYYY-MM-DD HH:MM] Stage: <1-6>  Actor: HUMAN | AI | HUMAN+AI | VALIDATOR
Action:        what was done
Input:         data version / config / prior decision it depended on
Decision:      what was chosen, and what was rejected
Evidence:      the numbers, the check that passed, or the file that proves it
Verification:  which rung of the ladder, and the result
Approval:      human consent, if the action required it
Risk:          what could still be wrong
Next:          what this unblocks
```

Failed experiments get entries too. A study whose ledger contains only successes is a study that
lost its own history. Version control the ledger with git where available; where not, keep dated
entries and never edit a past one — append a correction instead.

## Closing the project

Do not declare completion until all of the following hold:

```
[ ] Research question and hypothesis defined and unchanged, or changes versioned
[ ] Environment, data source, and data version recorded
[ ] Preprocessing pipeline exists as runnable code
[ ] EDA completed and reviewed jointly
[ ] Analysis method chosen by the human; results verified
[ ] Evaluation harness passing, with failures documented
[ ] Human interpretation checked against the evidence
[ ] Diligence checklist complete (references/diligence.md)
[ ] Reproducibility package assembled
[ ] Ledger complete, including failed attempts
[ ] Human has chosen where the assets live
```

The reproducibility package is whatever lets another researcher rerun this: code, configs, the
preprocessing pipeline, seeds, environment spec (`requirements.txt` / `environment.yml` /
Dockerfile), the evaluation harness, and a README stating how to reproduce and what the known
limitations are. Include the data itself only if licensing and privacy allow — otherwise ship the
acquisition script and the schema.

Finally, ask the human where the work should live: a shared repository, local only, or both. If a
repository, confirm its visibility and confirm that no sensitive data is being published. If both,
separate the shareable code and documentation from data that cannot be released.

Close with a short status summary: question, hypothesis, dataset version, analysis and model
version, verification status, storage destination, and known limitations.

## Attribution

The 4D Framework (Delegation, Description, Discernment, Diligence) and the three modes of AI
interaction are from the AI Fluency Framework by Rick Dakan and Joseph Feller with Anthropic,
Copyright 2025, released under CC BY-NC-SA 4.0. This skill is an application of that framework to
data-analysis research projects and is distributed under the same license.
