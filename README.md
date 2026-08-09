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
