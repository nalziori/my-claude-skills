# my-claude-skills

Personal Claude Code skill marketplace — lets these skills follow you to any
PC you log into, instead of being stuck on the machine they were created on.

## Skills in here

- **hackathon-agent-scaffold** — at the start of a hackathon like HackerRank
  Orchestrate, generates a tailored `CLAUDE.md` project brief and
  `eval_harness.py` scoring script (Korean + English) from the problem
  statement and data schema.
- **hackathon-interview-prep** — after the build is functionally done,
  runs a 4-step prep process for the live/AI-judge interview: a deep
  self-understanding walkthrough, a context-blind "fresh eyes" evaluator
  subagent, spoken mock Q&A, and a prepared self-directed question.
- **ael-ledger-setup** — designs and adds an Agent Execution Ledger (AEL) to
  an agent/pipeline project: an append-only SQLite structure recording every
  decision cycle (Planning → Execution → Evidence → Verification →
  Reflection → State) so decisions stay auditable after the fact.
- **ael-ssot-debug** — for projects that already have an AEL, helps debug
  why a specific past decision/cycle happened the way it did.
- **engineering_memory** — keeps a persistent, written record of decisions,
  experiments, regressions, and API/cost spend across a long-running
  research-and-build project, so rationale survives context compaction and
  session restarts.
- **python_venv_creater** — creates and configures a Python virtual
  environment (.venv) for a project: venv creation, pip upgrade, dependency
  install, Jupyter kernel registration, and VSCode settings wiring.
- **research_engine** — a research-first thinking protocol to load before
  any non-trivial build/debug/improvement task: restate goals, build a
  mental model, generate competing hypotheses, validate cheaply before a
  full eval, and leave a decision trace.

## Setup on a new PC

1. Make sure git is installed.
2. In Claude Code, add this repo as a plugin marketplace:
   ```
   /plugin marketplace add <this-repo-url>
   ```
3. Install the skill collection:
   ```
   /plugin install personal-skills@my-claude-skills
   ```
4. The skills are now available in Claude Code on this machine, and will
   trigger automatically based on their descriptions (or invoke directly,
   e.g. `/hackathon-agent-scaffold`).

## Updating

Edit a skill's `SKILL.md` (or assets) under `plugins/personal-skills/skills/`,
commit, and push. Run `/plugin marketplace update my-claude-skills` (or
reinstall) on each machine to pull the latest version.
