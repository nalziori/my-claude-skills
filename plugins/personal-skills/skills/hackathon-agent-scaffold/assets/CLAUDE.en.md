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

## 3-1. Output Contract — fill this in before writing code
> September Orchestrate feedback: state the contract up front, don't bolt it on later as asserts.
- Output columns/types: [allowed values and format per column]
- Cross-field rules (e.g. if status is X, field Y must be empty / amount must not exceed A): [...]
- **Single source of truth**: compute the core forecast/simulation once, and derive every output field together from the one selected decision. No separate per-field heuristics.
- Run `validate_row()` over all rules just before writing output. A row that fails is replaced with the safe default and logged.

## 3-2. Missing/Contradictory Evidence Policy and Model-Failure Fallback
- Precedence and conservative default when evidence is ambiguous or contradicts: [e.g. explicit amendment > newer same-source record > settled record > estimate; if still ambiguous, take the conservative side]
- Input validation rules per dataset field (allowed ranges, missing-value handling): [...]
- If a model call fails (quota, timeout, malformed JSON): retry, then treat that fact as "not enough evidence", apply the conservative default and keep going. One row's failure must never stop the whole run.
- Put 2-3 few-shot examples of conflicting inputs in the prompt (how to resolve, not only how to extract).
- If the pipeline is fixed-sequence, decide whether a small router (model picks among a limited set of tools/steps and justifies it) is needed, and record why in the Decision Log.
- When asking for debugging help, paste the raw error/stack trace, not a summary.

## 3-3. AEL usage rule
- Ledger file: `data/ael.db` (append-only, never dropped on rerun). Build it with the `ael-ledger-setup` skill at project start, before the first agent function.
- One cycle = one request/row. The Verification stage runs `validate_row()`.
- To debug a row or a low-confidence pattern: use the `ael-ssot-debug` skill first, then read code.
- Interview prep: the ledger is the evidence for "how did you verify this decision?".

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
