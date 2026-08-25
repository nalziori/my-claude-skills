# research-4d

A Claude Code skill that runs data-analysis research projects as human-led, AI-assisted
collaboration, governed by the AI Fluency 4D Framework.

**What it enforces.** A six-stage pipeline with explicit exit gates (definition → ingestion →
cleaning → EDA → modeling → interpretation), human ownership of the research question and the
final interpretation, verification at the cheapest sufficient level, consent before expensive
agent loops, and continuous recording of ethics, provenance, and reproducibility.

**Who it is for.** Researchers writing papers, theses, or reports where the analysis has to be
defensible — not one-off exploratory plots.

## Install

Copy this directory into your skills folder:

```
~/.claude/skills/research-4d/          # personal, all projects
.claude/skills/research-4d/            # project-local, checked into the repo
```

Restart Claude Code. It triggers automatically on research-shaped requests, or invoke it directly
with `/research-4d`.

## Layout

```
SKILL.md                      the operating protocol — always loaded when triggered
references/stages.md          per-stage detail and exit criteria — loaded on entering a stage
references/diligence.md       ethics, bias, causal language, disclosure, final harness
```

References are separate so the protocol stays cheap to load and the detail arrives only when the
relevant stage begins.

## Working files it maintains

```
research/PROJECT.md    the confirmed research brief — the contract
research/LEDGER.md     append-only record of decisions, verifications, and failures
```

## License and attribution

The 4D Framework (Delegation, Description, Discernment, Diligence) and the three modes of AI
interaction (Automation, Augmentation, Agency) are from the AI Fluency Framework by Rick Dakan and
Joseph Feller with Anthropic, Copyright 2025, released under CC BY-NC-SA 4.0.

This skill applies that framework to data-analysis research projects and is distributed under the
same license: **CC BY-NC-SA 4.0**. Attribution required, non-commercial use, share alike.
