---
name: hackathon-agent-scaffold
description: Scaffold a new AI-agent hackathon project (like HackerRank Orchestrate) by generating a customized CLAUDE.md project brief and an eval_harness.py scoring script, in both Korean and English, tailored to the specific problem statement, data schema, and labels just received. Use this skill whenever the user shares or pastes a new hackathon/agent-building problem statement and wants to get set up, scaffold the repo, prepare CLAUDE.md, build an evaluation harness, or otherwise start a 24-hour AI agent challenge — even if they don't explicitly say "skill", "scaffold", or name the files. Trigger on things like "오늘 문제 받았어, 세팅 좀 해줘", "이번 챌린지 내용 붙여넣을게, 준비해줘", "새 해커톤 시작하는데 CLAUDE.md 만들어줘", or a pasted problem statement followed by "이걸로 시작하자".
---

# Hackathon Agent Scaffold

Turns a freshly-received hackathon problem statement into a ready-to-work project: a `CLAUDE.md` brief that captures the problem and architecture principles, and an `eval_harness.py` that scores the agent's output — both in Korean and English. The four generic templates already encode hard-won lessons from past HackerRank Orchestrate submissions (trace-one-input self-checks, guardrail patterns, eval-loop logging, degenerate-strategy sanity checks) — your job is to adapt them to *this* problem, not to reinvent them from scratch.

## When this runs

The user has just received (or is about to receive) a hackathon problem statement — a domain, an input data schema, a decision the agent must make, and usually a success metric. They want a working project skeleton before they start coding, not after.

## Step 1 — Extract the problem shape

Read whatever the user gave you (pasted problem statement, email text, a linked doc) and pull out:

- **Domain / objective**: what is the agent deciding or producing? (e.g. "classify support tickets and decide reply vs escalate")
- **Input data**: format (CSV/JSON/Markdown corpus/images), where it lives, key columns or fields
- **Decision / label space**: the fixed set of allowed outputs, if any (e.g. `reply` / `escalate`), or the output schema if it's generative
- **id column**: whatever uniquely identifies each row/case
- **Success metric**: accuracy against a golden set, F1, something custom
- **Known edge cases or traps mentioned**: e.g. prompt-injection attempts in the data, ambiguous or incomplete rows, degenerate strategies that are explicitly invalid

If any of these are missing or unclear from what the user shared, ask — don't guess at the label space or success metric, since a wrong guess here makes both output files actively misleading. Everything else, use reasonable judgment and move forward.

## Step 2 — Customize CLAUDE.ko.md / CLAUDE.en.md

Start from `assets/CLAUDE.ko.md` and `assets/CLAUDE.en.md`. Fill in the bracketed placeholders (`[...]`) using what you extracted in Step 1 — objective, data location/format, success criteria, and what counts as an invalid/degenerate strategy.

Then adapt the **Architecture Principles** section to the domain:
- If the input is multi-modal (images + text), add a principle about how each modality is normalized and combined before the model call.
- If the data is a document/RAG corpus, add a principle about retrieval scope and what happens when nothing relevant is retrieved.
- If the problem statement mentions adversarial inputs (prompt injection, jailbreak attempts), keep and sharpen the existing guardrail principle — this is one of the most consistently rewarded patterns in past submissions.

Leave the **Trace-One-Input Self-Check**, **Eval Loop Log**, and **Decision Log** sections structurally intact — these are the parts that carry over regardless of domain and are what the AI-judge interview tends to probe. Don't compress or remove them to save space.

## Step 3 — Customize eval_harness_ko.py / eval_harness_en.py

Start from `assets/eval_harness_ko.py` and `assets/eval_harness_en.py`. At minimum, update the `--id-col` and `--label-col` defaults to match the real schema.

Then extend `sanity_check()` for this problem's actual label space where one is known — e.g. reject predictions with labels outside the allowed set, not just flag skewed distributions. If the success metric isn't plain accuracy (e.g. weighted F1, or a custom penalty for false-escalations), replace the `score()` body accordingly and say so in a comment — don't silently keep accuracy if it doesn't match what the problem asks for.

Keep `eval_loop_reminder()` — it's a low-cost nudge toward the build-run-inspect-fix-rerun habit that past write-ups consistently flag as separating a strong submission from a quick prototype.

Before handing the script back, run it once against a tiny synthetic sample (3-5 rows) you construct from the problem's schema, to confirm it actually runs against the real column names rather than just looking correct.

## Step 4 — Deliver

Produce all four files (`CLAUDE.ko.md`, `CLAUDE.en.md`, `eval_harness_ko.py`, `eval_harness_en.py`) as actual files in the project workspace, not just inline text — the user works with these as real project files from day one of the hackathon. Briefly note what you customized versus what stayed generic, so the user can spot anything you guessed wrong.
