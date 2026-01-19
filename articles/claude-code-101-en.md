Official Claude Code docs: https://code.claude.com/docs/

## Claude Code 101: a practical playbook for shipping real changes safely

This guide is a **Claude Code–specific** "101" for system developers. The goal is not theory—it's a set of repeatable workflows that produce **small diffs, fast feedback, and fewer regressions**.

---

## Think first (use Plan Mode, then execute)

Claude Code works best when the first step is **structuring the problem**, not typing instructions.

### Why this matters
If the request is broad, Claude will fill in gaps with "reasonable defaults." In engineering work, those defaults often become:
- unnecessary abstractions
- too many files
- hidden behavior changes  
**Rationale:** ambiguity increases solution space, and the model will explore it.

### What to do
1) **Write the target state (acceptance criteria) before asking for code.**  
   **Rationale:** Claude is strongest when optimizing for an explicit "done," not an implied one.

2) **Use Plan Mode for anything that affects architecture, data, auth, or interfaces.**  
   In Claude Code, enter Plan Mode (commonly **Shift+Tab twice** depending on setup).  
   **Rationale:** planning forces explicit boundaries and reduces surprise edits.

3) **Ask for options and tradeoffs first, then choose.**  
   Example prompt:
   - "List 2–3 viable designs, call out risks, and recommend one. Do not write code yet."  
   **Rationale:** the fastest path is often picking the right approach early.

### Replace vague with specific
Bad:
- "Build an auth system."

Good:
- "Add email/password auth using the existing User model; store sessions in Redis with 24h expiry; protect routes under `/api/protected`; no new dependencies; add integration tests."

**Rationale:** specificity prevents overreach and creates a verifiable output.

---

## Architecture isn't optional (it's how you constrain the model)

Claude can generate working code that violates your system's invariants. The fix is not "better code generation." The fix is **architectural constraints up front**.

### What to include in your plan request
- **Boundaries:** what modules can/can't touch each other
- **Invariants:** what must remain true
- **Non-goals:** what must not change
- **Validation:** commands that prove it works

**Rationale:** constraints act like guardrails; without them, Claude invents structure.

---

## CLAUDE.md: your highest-leverage file

`CLAUDE.md` is a Markdown file Claude Code reads at the start of a session. It functions as **persistent repo-specific instruction**.

### Why it matters
It turns repeated corrections into a stable contract:
- "use this test command"
- "don't reformat unrelated files"
- "avoid new abstractions"
- "follow these conventions"

**Rationale:** durable guidance reduces prompt length and increases consistency across sessions.

### How to write a good CLAUDE.md
**Keep it short.**  
If you include too much, Claude will ignore instructions unpredictably.  
**Rationale:** instruction overload creates priority conflicts.

**Make it repo-specific.**  
Avoid generic explanations ("what components are"). Include the weird, local rules.  
**Rationale:** Claude already knows general patterns; it needs your *specific* ones.

**Explain "why," not only "what."**  
- "Use TypeScript strict mode because implicit any caused production bugs."  
**Rationale:** the "why" helps Claude make better judgment calls in edge cases.

**Update it continuously.**  
Any time you correct the same mistake twice, add an instruction. Claude Code supports quick ways to capture guidance (often via a shortcut such as `#`, depending on configuration).  
**Rationale:** this compounds—each fix prevents future rework.

### A practical CLAUDE.md starter (copy/paste)
```md
# CLAUDE.md (project instructions)

## Goals
- Produce minimal, reviewable diffs.
- Prefer existing patterns in this repo.

## Non-goals
- Do not introduce new dependencies without explicit request.
- Do not reformat unrelated files.
- Do not create new abstractions unless asked.

## Commands (run after edits)
- Format: <cmd>
- Lint: <cmd>
- Typecheck: <cmd>
- Tests: <cmd>

## Architecture constraints
- Keep domain logic out of HTTP handlers.
- No DB access in middleware unless explicitly required.
- Keep public API backwards compatible by default.

## Working style
- Start with a 3–7 step plan.
- After each step: summarize diff + commands run + remaining risks.
- If uncertain: stop and ask for a decision.
```

---

## "Ultrathink" mode (quality-first mindset)

Some teams use a short, high-signal "quality bar" in their project guidance to bias Claude toward **deliberate planning, careful reading, and minimal complexity**. This can live in `CLAUDE.md` (or in a separate `QUALITY.md` referenced from `CLAUDE.md`) as long as it stays concise.

### Principles to encode (and why they help)

- **Think different:** question assumptions and consider simpler architectures before implementation.  
  **Rationale:** the first working solution is often not the best fit for long-lived systems.

- **Obsess over details:** read existing code like a specification—follow established patterns and naming.  
  **Rationale:** consistency reduces integration bugs and keeps diffs reviewable.

- **Plan like a designer:** write a short plan that makes interfaces and invariants explicit before editing files.  
  **Rationale:** explicit boundaries prevent plausible-but-wrong code generation.

- **Craft, don't sprawl:** keep functions and abstractions minimal; avoid introducing new layers unless requested.  
  **Rationale:** unnecessary indirection increases maintenance cost and hides defects.

- **Iterate relentlessly:** validate after each step (tests, screenshots, comparisons) and refine until it's correct and clean.  
  **Rationale:** frequent feedback catches regressions early and shortens the path to "done."

- **Simplify ruthlessly:** remove complexity when it doesn't buy measurable value.  
  **Rationale:** simpler systems fail in fewer ways and are easier to operate.

### Tooling cues worth capturing

- **Use your tools as instruments:** lean on bash commands, MCP servers, and custom slash commands for repeatable workflows.  
  **Rationale:** automation reduces manual copy/paste errors and saves time.

- **Use Git history as context:** check prior approaches and conventions before inventing new ones.  
  **Rationale:** history reveals intent and reduces churn from "new but inconsistent" implementations.

- **Treat mocks/screenshots as specs when available:** implement to the visual/behavioral target.  
  **Rationale:** concrete targets reduce ambiguity and rework.

- **Use multiple Claude sessions intentionally:** separate planning vs execution, or isolate unrelated concerns.  
  **Rationale:** separation reduces context bleed and improves focus.

---

## Context windows degrade earlier than you think

Even with large context windows, quality tends to drop before you "fill the bar." Symptoms include:
- repeating the same mistake
- losing track of constraints
- hallucinating structure you never requested

**Rationale:** more context increases competition for attention; important details lose salience.

### Practical context management techniques

**1) One conversation per task**  
Don't use the same session to build auth and refactor database layers.  
**Rationale:** unrelated context bleeds and creates wrong assumptions.

**2) Use external memory files**  
Have Claude write to `SCRATCHPAD.md`, `plan.md`, or `devdocs/progress.md`.  
**Rationale:** files persist across sessions and anchor the "truth" in the repo.

**3) Copy–paste reset workflow (fast and effective)**  
When things get bloated:
- run `/compact` to get a summary
- run `/clear` to reset context
- paste back only the critical plan + constraints + current errors

**Rationale:** a small, clean context often outperforms a large, degraded one.

**4) Know when to clear**  
If the session is confused, reset early. `CLAUDE.md` still provides baseline guidance.  
**Rationale:** debugging a confused context is slower than restarting with a clean brief.

### Adopt the right mental model
Claude is effectively stateless unless you externalize state.  
**Rationale:** expecting memory that isn't there creates inconsistent results.

---

## Prompting: treat it like engineering communication

Prompting is not magic. It is requirements + constraints + verification.

### Use a repeatable prompt structure
**Request template**
- Goal
- Context (files/paths)
- Constraints / non-goals
- "Done" criteria
- Ask for a plan first (then code)

**Rationale:** structured input reduces rework and makes outputs reviewable.

### Always include "what not to do"
Claude often defaults to extra abstraction. If minimalism matters, say so:
- "Keep this simple. No new files unless necessary. No abstractions I didn't ask for."

**Rationale:** negative constraints prevent scope expansion.

### Include "why" when it affects tradeoffs
Examples:
- "Runs on every request → optimize for latency."
- "Prototype to throw away → keep it minimal."

**Rationale:** "why" drives correct tradeoffs.

---

## Bad input → bad output (without the hostility)

When output is consistently wrong, the fix is usually:
- insufficient constraints
- missing acceptance criteria
- missing repo context
- tasks too large (not decomposed)

**Rationale:** the model can't infer constraints you didn't provide.

### Fast diagnostic checklist
If Claude misses the mark, check whether the prompt contained:
- explicit "done" criteria
- explicit non-goals
- file paths/entrypoints
- validation commands
- a staged plan request

**Rationale:** missing any of these increases ambiguity and surprises.

---

## Model choice workflow (keep it practical)

Claude Code often exposes different models with different tradeoffs (speed vs deeper planning). A reliable pattern:

- Use a stronger reasoning model for **planning and tradeoffs**
- Use a faster model for **implementation once the plan is locked**

**Rationale:** planning quality is leverage; execution speed matters after decisions are made.

---

## MCP, hooks, slash commands, and configs: use features that remove toil

Claude Code has power features. The point isn't "enable everything." The point is **remove repeated friction**.

### MCP (Model Context Protocol)
Use MCP when you repeatedly copy data from:
- GitHub
- Slack
- issue trackers
- databases/APIs

**Rationale:** automating context ingestion reduces manual errors and saves time.

### Hooks
Hooks can run commands before/after changes:
- formatter on edited files
- typechecking after edits
- test subset after a step

**Rationale:** hooks convert good intentions into automatic enforcement.

### Custom slash commands
Create reusable prompts as commands via `.claude/commands/*.md`:
- `/review-pr`
- `/debug-failure`
- `/refactor-module`
- `/write-tests`

**Rationale:** standardizing prompts increases consistency across the team.

### Settings/configuration
Use config to align behavior:
- default commands
- preferred style (small diffs, stop-and-ask on uncertainty)
- guardrails (avoid new deps, avoid broad refactors)

**Rationale:** configuration reduces prompt overhead and drift.

---

## When Claude gets stuck: break the loop intentionally

Stuck patterns:
- repeating the same fix
- confident but wrong changes
- endless "one more attempt"

### What to do instead

**1) Reset context (`/clear`)**  
Then re-provide only:
- task brief
- constraints
- the specific error

**Rationale:** stuck behavior often correlates with polluted context.

**2) Make the task smaller**
Ask for one of:
- a minimal reproduction
- a single-file fix
- a test-first change

**Rationale:** smaller search spaces reduce failure modes.

**3) Show a concrete example**
- "Here is the desired output format; apply it elsewhere."

**Rationale:** examples are unambiguous success metrics.

**4) Reframe**
- "Treat this as a state machine."
- "Write this as pure functions with explicit inputs/outputs."

**Rationale:** some framings map better onto the model's reasoning.

---

## Build systems, not one-off interactions (headless mode)

Claude Code can be used beyond interactive sessions. In particular:
- headless runs (e.g., via a `-p` prompt flag in some setups)
- scripting chained workflows
- automated PR review / doc updates

**Rationale:** automation turns individual wins into repeatable throughput.

### A safe automation pattern
- run on a narrow scope (single directory / file patterns)
- log output
- require CI pass before merge
- keep human review in the loop for risky domains

**Rationale:** bounded automation is auditable and reduces unintended changes.

### The improvement flywheel
- Claude makes a mistake
- capture the rule in `CLAUDE.md` or a command template
- add a hook/check to prevent recurrence

**Rationale:** systematic fixes compound.

---

## TL;DR (Claude Code 101)

- **Think first, then type:** Plan Mode consistently produces better outcomes.  
  **Rationale:** planning constrains the solution space.
- **Write architecture constraints:** boundaries + invariants + non-goals.  
  **Rationale:** prevents plausible-but-wrong implementations.
- **`CLAUDE.md` is leverage:** keep it short, repo-specific, and updated.  
  **Rationale:** durable instructions improve every session.
- **Context degrades early:** scope sessions, externalize memory, reset with `/compact` + `/clear`.  
  **Rationale:** smaller clean context beats large noisy context.
- **Prompt like an engineer:** be explicit about done criteria and what not to do.  
  **Rationale:** reduces overengineering and rework.
- **Use MCP/hooks/commands when they remove toil.**  
  **Rationale:** automation makes quality repeatable.
- **When stuck, change approach:** reset, simplify, show examples, reframe.  
  **Rationale:** loop-breaking beats brute force.
