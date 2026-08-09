# Project: [Problem name goes here]

## 1. Objective
- What are we building: [e.g. an agent that classifies support tickets across product domains and decides reply/escalate]
- Success criteria: [e.g. accuracy against a hidden golden set, minimizing false-escalations — fill in as soon as the problem statement arrives]
- What's okay to fail / what must not happen: [e.g. blanket strategies like "always escalate" or "always reply" are invalid]

## 2. Data
- Location: `data/` (update once the real path is known)
- Format: [CSV / Markdown corpus / JSON, etc.]
- Watch-outs: [PII, noise, known edge cases, etc.]

## 3. Architecture Principles
- This project follows these principles:
  1. Separate decision logic from execution logic (classify → decide → act pipeline)
  2. Every decision must carry evidence/citation — no unsupported answers
  3. On failure, fall back to a safe default (e.g. escalate to human)
  4. Inputs suspected of prompt injection / jailbreak attempts get flagged and routed to a human, not silently obeyed
  5. Avoid letting a single LLM call become the entire architecture — split input loading/normalization, context construction, model call, response parsing, schema validation, label enforcement, retries, logging, and flag decisions into separate responsibilities

## 4. Trace-One-Input Self-Check
> Before explaining the system to anyone, pick one input and confirm you can answer these:
- [ ] Where is it read?
- [ ] How is it cleaned?
- [ ] What context gets added?
- [ ] Where is the model called?
- [ ] What schema does the response follow?
- [ ] What does the code validate after the response?
- [ ] What gets logged?
- [ ] When does it retry / abstain / route for review?
- [ ] Where is the final output written?

## 5. Repo Layout
```
code/           # actual agent code
data/           # input data (may need to be excluded from submission — check the rules)
eval/           # evaluation harness and test cases
output/         # final predictions (output.csv, etc.)
transcripts/    # AI chat logs (log.txt)
```
- Avoid file names like `helper`, `final`, `utils`, `test2` — name files after their role

## 6. Eval Loop Log
> Record the "build → run → inspect failures → fix → rerun" cycle here.
> The loop itself matters more than the size of the benchmark.

- [Iteration N] Run result: ... / Failure pattern found: ... / What was changed: ...

## 7. Decision Log
> Add a line each time you and Claude Code settle on "why this choice."
> This doubles as interview prep and keeps the reasoning explicit in the transcript.

- [timestamp] Decision: ... / Reason: ... / Alternatives rejected: ...

## 8. Connected Tools / MCP
- [List MCPs in use and why each is needed, one line each]

## 9. Open Questions
- [ ] ...
