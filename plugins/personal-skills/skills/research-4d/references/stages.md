# The six stages in detail

Read the section for the stage you are entering. Each stage lists its goal, the interaction mode,
the work, and the exit gate. Do not cross an exit gate with an unmet criterion — name what is
missing and stop.

---

## Stage 1 — Research Definition & Environment

**Goal.** Turn a vague intention into a testable research question, and know what machine the work
will run on.
**Mode.** Augmentation. The human supplies the question; you sharpen it.

### Work

Confirm the research brief (see SKILL.md) and restate it in structured form:

```
Research Question
Hypothesis
Population / unit of analysis
Outcome
Predictors
Objective
Constraints
Success criteria
```

Show it back and get explicit confirmation. Once confirmed, do not alter it without a versioned
change entry.

Then survey the environment, since it constrains every downstream tooling choice: OS, CPU, RAM,
GPU and VRAM, free storage, Python version, key library versions, CUDA/cuDNN, Docker, git. Record
what you actually observed, not what you assume is installed.

Propose analysis tooling matched to the data scale and question — pandas or Polars for in-memory
work, PySpark or Dask when it will not fit, statsmodels for inference, scikit-learn or
PyTorch/TensorFlow for modeling, SQL where the data already lives in a database. Present the
tradeoff; let the human choose. A tool the researcher cannot debug is the wrong tool regardless of
benchmarks.

### Exit gate

- [ ] Research question and hypothesis confirmed by the human
- [ ] Objective, population, outcome, and predictors written down
- [ ] Success criteria defined
- [ ] Environment recorded
- [ ] Tooling selected by the human
- [ ] `research/PROJECT.md` written

---

## Stage 2 — Data Ingestion & Storage

**Goal.** Get the data, know exactly where it came from, and be able to say which version was
used.
**Mode.** Automation, with a Diligence gate before any collection.

### Work

Ask first: is the data already available?

**If it exists**, profile it before anything else: location, format, size on disk, row and column
counts, variable list and types, origin, collection date, version, and whether it contains
personal information. Report what you found; do not modify anything yet.

**If it does not exist**, propose collection routes — an API, a public data portal, a database
export, an established public dataset, web scraping, or human-supplied data — and run the
Diligence check in `diligence.md` *before* collecting anything, not after. Scraping and social
media data in particular need a terms-of-service and copyright review first.

Record for every source:

```
Source
Collection method
Collection date
License / terms of use
Consent requirement
Privacy risk
Expected size
Storage format
Version identifier
```

Build a collection harness that checks, at minimum: source legitimacy, license compliance,
collection success rate, schema validity, duplicate rate, missingness, presence of expected
fields, file integrity, PII detection, and version identification. If a legal or ethical check
fails, stop collecting and report to the human — do not "collect now, filter later."

Store raw and derived data separately, and treat raw as immutable:

```
data/
├── raw/        # never modified after landing
├── interim/    # intermediate transformations
└── processed/  # analysis-ready
```

Choose the format for the scale: CSV for small and human-readable, Parquet for anything large or
columnar, a database when the data outlives one analysis.

### Exit gate

- [ ] Data acquired, or collection plan approved by the human
- [ ] Source, license, and collection date recorded
- [ ] Data version recorded
- [ ] Raw data stored immutably
- [ ] Collection harness passing
- [ ] PII status determined and documented

---

## Stage 3 — Data Cleaning & Preprocessing

**Goal.** Make the data analysis-ready without silently destroying evidence.
**Mode.** Automation for execution, human sign-off for anything destructive.

### Work

Profile for problems before fixing any: missing values and their pattern, duplicates, wrong types,
invalid or impossible values, outliers, inconsistent formats, potential target leakage, class
imbalance, unexpected categories, and out-of-range values.

Never delete data unilaterally. Propose each treatment in this form:

```
Problem:          what is wrong, and where
Evidence:         counts, percentages, examples
Proposed action:  what you want to do
Expected impact:  rows/columns affected, effect on the analysis
Risk:             what this could destroy or bias
```

These always need explicit human approval: outlier removal, dropping rows for missingness,
dropping variables, downsampling, and any change to the sampling frame. Each of them can change a
conclusion, and each is invisible in the final numbers.

Then implement the approved transformations — imputation, encoding, scaling, normalization,
feature transformation, resampling. Everything must be runnable code with recorded parameters,
never a sequence of manual steps. The test is simple: can someone rerun it from the raw data and
get a byte-identical result?

Watch the leakage boundary specifically. Fit scalers, imputers, and encoders on training data
only, then apply to validation and test. Fitting on the full dataset before splitting is the most
common way an AI-assisted pipeline produces an optimistic, wrong result.

Optionally, propose a statistics-persona review of the cleaning decisions — but this is a loop, so
the consent rule in SKILL.md applies.

### Exit gate

- [ ] Data quality report written
- [ ] Every destructive decision explicitly approved
- [ ] Preprocessing pipeline saved as runnable code
- [ ] Leakage boundary verified
- [ ] Processed data version recorded
- [ ] Rationale for each major decision in the ledger

---

## Stage 4 — Exploratory Data Analysis

**Goal.** Understand the data well enough to choose the right analysis — and to notice what would
invalidate it.
**Mode.** Augmentation. This stage is where the researcher's domain knowledge does work no model
can substitute for.

### Work

Compute descriptive statistics: mean, median, variance, standard deviation, skewness, kurtosis,
quantiles, and frequencies for categoricals. Examine relationships with Pearson or Spearman
correlation as the distribution warrants, cross-tabulations, group comparisons, and distribution
comparisons. Label correlations as correlations, in the output and in the commentary.

Visualize — histograms, scatter plots, box plots, bar charts, heatmaps, density plots. Sample
sensibly when the data is too large to plot whole, and say what the sample was.

Then run the insight session rather than issuing conclusions:

```
AI findings          →  what the data shows, stated flatly, no interpretation
Human interpretation →  what the researcher makes of it, with domain knowledge
AI critique          →  what the data does and does not support in that reading
Joint interpretation →  what you both agree the evidence sustains
```

Tie every notable observation back to the hypothesis. An interesting pattern unrelated to the
research question is a note for later, not a finding — flag it as such and move on. Scope creep in
EDA is how a focused study becomes an unpublishable fishing expedition.

### Exit gate

- [ ] EDA report produced
- [ ] Key variable candidates identified
- [ ] Distributions and anomalies documented
- [ ] Observations linked to the hypothesis
- [ ] Joint interpretation recorded
- [ ] Candidate analysis methods listed for stage 5

---

## Stage 5 — Advanced Analytics & Modeling

**Goal.** Test the hypothesis, and if modeling, build something whose performance number is
trustworthy.
**Mode.** Augmentation, with the method decision reserved to the human.

### Work

Propose several candidate methods — regression, t-test, ANOVA, chi-square, correlation analysis,
logistic regression, tree-based models, neural networks, whatever fits — and for each state:

```
Method
Why it applies here
Assumptions it requires (and whether this data meets them)
Advantages
Limitations
Expected output
How it would be validated
```

The human chooses. Provide a comparison table if the choice is hard. Do not settle the core
analysis method yourself — that decision belongs to whoever defends the paper.

Then work as a team, not as a request queue:

```
Human research direction → AI analysis proposal → Human review → Experiment
→ AI result → Human interpretation → AI critique → Decision
```

For any model, record before running: train/validation/test split strategy, cross-validation
scheme, hyperparameter configuration, random seed, the baseline you are beating, and the
evaluation metrics with their thresholds. A model without a baseline has no demonstrated value —
compare against the obvious dumb predictor at minimum.

Build an evaluation harness covering statistical validity, metric thresholds, cross-validation
consistency, data leakage, overfitting signals, baseline comparison, reproducibility from seed,
and error analysis on the failures. Run it on every candidate, not just the winner.

Record failed experiments with the reason they failed. They are evidence about the problem, they
prevent the next person from repeating them, and their absence from a write-up is itself a form of
selective reporting.

An expert-persona review loop fits naturally here — typically review, critique, revision. It is
still a loop: estimate the cost, propose the rounds, and get consent first.

### Exit gate

- [ ] Analysis method selected by the human, with rationale
- [ ] Analysis and model results produced
- [ ] Evaluation metrics computed against a baseline
- [ ] Evaluation harness passing
- [ ] Failed experiments documented with reasons
- [ ] Final analysis and model version recorded
- [ ] Seeds, hyperparameters, and splits recorded

---

## Stage 6 — Interpretation & Reproducibility

**Goal.** Answer the research question honestly, and leave something another researcher can rerun.
**Mode.** Augmentation, human first.

### Work

**The human interprets first.** Do not lead with your own conclusion — an AI-supplied
interpretation anchors the researcher and quietly becomes theirs. Ask:

```
What do you think this result means for your research question?
Is your hypothesis supported, and how strongly?
What are the limitations?
Can any of this be read causally? Why or why not?
```

**Then validate their interpretation against the evidence.** Check whether it matches the actual
output, whether statistical significance is being overstated, whether correlation has become
causation, whether any claim outruns the data, whether uncertainty is expressed, and whether model
performance is being oversold. Do not simply rewrite their reading — show the evidence and let
them revise. Where you disagree, cite the number you are disagreeing with.

If iteration is needed — interpretation, evidence check, critique, revision, final — that is a
loop. Consent rule applies.

Produce publication assets as needed: high-resolution figures (300 DPI or better for print),
confusion matrices, performance plots, and result tables. Label axes and state units and sample
sizes on every figure.

Assemble the reproducibility package:

```
code/            analysis and pipeline source
configs/         parameters, seeds, thresholds
models/          trained artifacts, versioned
reports/         findings and figures
validation/      the evaluation harness and its results
environment/     requirements.txt / environment.yml / Dockerfile
README.md        how to reproduce, and known limitations
```

Include data only where licensing and privacy permit; otherwise ship the acquisition script and
the schema so the pipeline can be rerun against a legitimate copy.

### Exit gate

- [ ] Human interpretation recorded first
- [ ] Interpretation validated against evidence
- [ ] Causal language audited
- [ ] Uncertainty and limitations stated explicitly
- [ ] Publication assets generated
- [ ] Reproducibility package complete and tested from a clean state
- [ ] AI-use disclosure drafted (see diligence.md)
