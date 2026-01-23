# Vibe Engineering 101
**Version 1.0** | 2026-01-22
*A practical guide for system developers getting started with agentic development*

Agentic development is less about "AI that writes code" and more about designing a reliable loop: a model proposes changes, tools validate them, and feedback drives the next iteration. This article is a field guide for building that loop so it produces useful software—consistently.

The goal here is not to romanticize "vibe coding," but to make it operational: clear constraints, fast feedback, and repeatable outcomes.

---

## 1) What an "agent" actually is

A useful working definition is:

**An agent runs tools in a loop to achieve a goal.**

From an engineering perspective, that's intentionally unglamorous. The system is typically:

1. Provide a goal + constraints  
2. Model proposes actions (edit files, run commands, inspect outputs)  
3. Tools run (tests, linters, builds, search, execution)  
4. Results go back into the loop  
5. Repeat until the acceptance criteria are satisfied

This simplicity is good news: it means agentic systems are *engineerable*. You can improve them by improving the loop, not by treating the model as magic.

---

## 2) Your context window is your "RAM"

LLMs don't "remember" your repository—at any moment, they operate on the tokens you've provided (plus whatever your tooling injects). Practically:

- **Everything that matters must be in context** (or reliably retrievable via tools).
- **More context is not always better.** Overstuffed contexts increase confusion, tool misuse, and subtle errors.
- **You need to manage what enters the loop.**

### Practical rules of thumb
- Avoid letting tools dump huge blobs of logs, diffs, or entire repos into the prompt.
- Keep feedback **minimal and actionable** (more on this in the harness section).
- If your agent/tooling auto-injects context, learn what it includes and how to tune it.

### A useful mental model
Treat the context window like scarce memory in older systems. If you let it fill with noisy logs and redundant information, you'll degrade performance the same way a constrained machine does when starved of resources.

---

## 3) The great decoupling: typing code vs engineering systems

Agentic development amplifies a shift many developers already experience with seniority:

- **Programming (typing code)** becomes cheaper.
- **Engineering (design, constraints, testing, tradeoffs)** becomes more valuable.

Models are often very strong at:
- syntax and boilerplate
- translating intent into implementation
- generating variations quickly
- working across unfamiliar ecosystems (with guidance)

They're still weak or unreliable at:
- understanding your business context by default
- making product tradeoffs without clear priorities
- guessing non-obvious system constraints
- maintaining coherence over long, messy histories

So the role changes: you spend more time on specs, acceptance criteria, tests, and architecture—and less time on keystrokes.

---

## 4) You are now Tech Lead + QA Lead

A productive framing is:

- **You define "done."**
- **You design the feedback loop.**
- **You review outcomes, not every line.**

Models behave like extremely fast collaborators with no long-term memory. They can move quickly, but they need:
- clear constraints
- crisp definitions of success
- deterministic feedback (tests, lint, build)
- guardrails against drifting

This is the core skill: **build "model CI" into your workflow**.

---

## 5) Stop fighting the model—build a better harness

A common failure mode is treating the model like a junior developer you must micromanage in real time. That creates a human bottleneck and reduces throughput.

Instead of manually fixing formatting, names, or tiny style issues:
- encode rules into tooling (formatter/linter)
- let the agent run the tooling
- use failures as feedback signals

When the agent goes in the wrong direction, assume one of these is true:
1. **The plan was under-specified.**
2. **The acceptance criteria were vague.**
3. **The feedback loop is weak or noisy.**

The fix is rarely "watch harder." It's usually:
- improve the spec
- tighten the tests
- reduce noise in outputs
- retry cleanly

---

## 6) Project setup is everything

The best time investment you can make is a repo that an agent can operate without confusion. A **repository harness** is the infrastructure that makes an agent work reliably.

### Hard requirement: one command to validate
Your project should build, test, and lint with **a single command**.

**Node.js/TypeScript:**
```bash
npm run check  # Runs: build + test + lint
```

**Python:**
```bash
make check  # Runs: pytest + black --check + mypy
```

**C#/.NET:**
```bash
dotnet build && dotnet test && dotnet format --verify
```

**Rust:**
```bash
cargo test && cargo fmt --check && cargo clippy
```

If validation requires tribal knowledge ("export this var," "run this in that directory," "install this system dependency manually"), your loop will waste context and time re-discovering it—over and over.

### Setup checklist

**One-command validation:**
- [ ] Create a command (e.g., `make check`, `npm run check`, `./scripts/ci.sh`) that runs build, tests, linting, and formatting
- [ ] Command works the same in CI and locally
- [ ] Command provides clear exit code (0 = success, != 0 = failure)

**Deterministic tests:**
- [ ] Tests give the same results every time (no race conditions, no timestamps in assertions)
- [ ] Tests can run in parallel without conflicts
- [ ] Tests are isolated (no shared state between tests)

**Clear feedback:**
- [ ] On success: minimal logs (e.g., "✅ 1000 tests passed" instead of 1000 lines of "ok")
- [ ] On failure: actionable logs showing the failing assertion, relevant diff, minimal stack trace, relevant file/line

**Stable scripts:**
- [ ] No "tribal knowledge" requirements
- [ ] Scripts work in Docker/CI the same way as locally
- [ ] Paths are relative or via environment variables

### Example: package.json (Node.js)

```json
{
  "scripts": {
    "check": "npm run build && npm run test && npm run lint",
    "build": "tsc",
    "test": "jest",
    "lint": "eslint . --ext .ts,.tsx",
    "format": "prettier --check ."
  }
}
```

### Example: Makefile (Python)

```makefile
.PHONY: check build test lint format

check: build test lint format
	@echo "✅ All checks passed"

build:
	python -m build

test:
	pytest

lint:
	ruff check .

format:
	black --check .
```

### Example: scripts/ci.sh (Bash)

```bash
#!/bin/bash
set -euo pipefail

echo "Building..."
npm run build

echo "Running tests..."
npm test

echo "Linting..."
npm run lint

echo "✅ All checks passed"
```

### Log filtering for agents

Agents read all output as feedback. Treat logs as an interface to an automated collaborator:

**Good: Concise on success**
```
✅ 1000 tests passed in 2.3s
```

**Bad: Noisy on success**
```
test 1: ok
test 2: ok
test 3: ok
... (997 more lines)
```

**Good: Actionable on failure**
```
FAIL: src/auth.test.ts:42
Expected: "user@example.com"
Received: "admin@example.com"
```

**Bad: Messy on failure**
```
[1000 lines of stack trace and compiler output]
```

### Determinism examples

**Problem: Non-deterministic tests**

```javascript
// Bad: uses current time
expect(result).toBe(new Date().toISOString());

// Good: deterministic
expect(result).toBe("2026-01-14T12:00:00Z");
```

**Problem: Race conditions**

```python
# Bad: can fail sometimes
def test_concurrent():
    results = []
    threads = [Thread(target=worker) for _ in range(10)]
    # ...

# Good: isolated or explicit synchronization
def test_concurrent():
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(worker, range(10)))
    # ...
```

This is "context engineering" in practice: design the I/O so the model sees signal, not noise.

---

## 7) Trust the loop, not your eyes

Agentic workflows scale when you can let the agent run without constant supervision.

To get there, you need:
- deterministic builds
- reliable tests
- linters/formatters
- clear exit codes
- stable scripts

A strong harness makes it safe to delegate:
- the agent changes code
- runs validation
- reads the failures
- iterates until green
- presents a summary and the final diff

Your role becomes verification-by-contract: "Does it meet the spec and pass the checks?"

---

## 8) Design for black boxes

Agentic development rewards modularity.

Favor components that are:
- small
- testable in isolation
- defined by clear inputs/outputs
- swappable without rewriting the world

Think "black box modules," not necessarily microservices:
- a CLI tool with stable flags
- a library with a narrow interface
- a service with a strict API boundary
- a pipeline stage with explicit artifacts

This reduces the amount of code the model must keep coherent at once and makes refactors safer.

---

## 9) CLI over IDE (for agents)

IDE integrations can be convenient, but the CLI has structural advantages for agentic work:

- **Discoverability:** `--help` teaches tools without extra context
- **Determinism:** scripts behave the same in CI as locally
- **Transparency:** stdout/stderr is an explicit interface you can tune
- **Composability:** easy to chain steps into one command

A good CLI-first workflow also makes it easier to run multiple agent sessions in parallel, since each session can operate through scripts rather than UI state.

If your environment is non-POSIX (or differs from what your tooling expects), consider:
- WSL
- devcontainers
- standardized shell scripts
- consistent path handling

The goal is not "one OS is best," but "remove friction that creates tool failures and noisy logs."

---

## 10) TDD becomes unusually effective with agents

Classic, strict Test-Driven Development can feel expensive for humans. With agents, the economics shift because tests become a steering wheel:

1. Write a failing test (or a failing check)
2. Let the agent implement the change
3. Iterate until green

This works especially well when:
- requirements are crisp
- edge cases are testable
- success is observable via assertions

### Guard against "cheating"
Agents may sometimes satisfy tests in shallow ways (mocking too much, hardcoding, bypassing logic). Countermeasures:
- add property-based tests where appropriate
- test multiple cases (not just "happy path")
- verify integration behavior, not only unit behavior
- include negative tests and invariants

---

## 11) Golden master testing for ports and refactors

When you're migrating systems or doing large refactors, golden master testing can be extremely effective:

- instrument the old system to emit deterministic traces (decisions, key state, outputs)
- save the trace as the "golden" file
- implement the new system
- ensure it matches the golden trace byte-for-byte (or via a normalized comparator)

This is powerful for:
- language migrations
- parser/serializer rewrites
- algorithm refactors
- "same behavior, different implementation" projects

If traces contain nondeterministic values (timestamps, pointers, random seeds), normalize them.

---

## 12) Spend time on planning (and make it reusable)

Agents benefit from plans that are:
- staged
- explicit about constraints
- explicit about "done"
- written down inside the repo

A good plan answers:
- what are we building?
- what are the non-goals?
- what are the interfaces?
- what are the invariants?
- what tests prove correctness?
- what order should changes land?

Models are also useful as planning assistants:
- ask for architectural alternatives
- request risk lists
- generate a phased implementation proposal
- identify missing acceptance criteria

But the plan must ultimately reflect *your* constraints and priorities.

---

## 13) DevDocs: surviving context resets

Long sessions degrade. A practical technique is to keep lightweight "agent handoff" docs in the repo, e.g.:

```
devdocs/
  plan.md
  progress.md
  decisions.md   (optional)
  notes.md       (optional)
```

Suggested contents:

**devdocs/plan.md**
- goals / non-goals
- architecture sketch
- phases
- acceptance criteria
- commands to run

**devdocs/progress.md**
- current state
- what's done (checkboxes)
- what's next
- known issues
- links to relevant files

When a session gets messy or the context fills up:
- start a fresh session
- point the agent at `devdocs/plan.md` + `devdocs/progress.md`
- continue with a clean slate

Key mindset: **plans and constraints are durable; code is replaceable.**

---

## 14) Accumulation and "slop" risk

A real concern in agentic development is long-term code quality drift:
- inconsistent patterns
- overgrown abstractions
- duplicated logic
- unclear boundaries

Mitigations:
- enforce formatting and linting
- require tests for changes
- maintain an architecture/decisions log
- refactor deliberately in phases
- periodically "re-derive" modules from a clean spec (when warranted)
- keep modules small and replaceable

Treat the agent like a high-throughput contributor: without governance, entropy accumulates.

---

## 15) Beyond coding: where agents shine

Agentic loops are often most valuable for work that is:
- necessary but not intellectually central
- highly iterative
- tool-driven
- easy to validate

Examples:
- fixing CI failures
- updating build scripts
- repository hygiene (lint, formatting, dependency upgrades)
- researching unfamiliar codepaths
- generating minimal repros
- writing migration scripts
- operational troubleshooting (when safe and controlled)

The common theme: the loop has clear tooling feedback and bounded risk.

---

## 16) Sub-agents and delegation patterns

One scaling pattern is separating:
- **exploration** (read code, map flows, identify files)
from
- **execution** (apply changes, run checks, refine)

You can model this as:
- a "scout" agent that returns a short report:
  - where the relevant logic lives
  - what the call graph looks like
  - what to change and why
- a "builder" agent that implements and validates
- a "reviewer" step that summarizes diffs and risks

This helps control context growth and reduces thrash.

---

## 17) A practical starter checklist

If you want agentic development to feel productive quickly, start here:

**Repository harness**
- [ ] Single command: build + test + lint  
- [ ] Clear scripts in `./scripts` or `Makefile`
- [ ] Minimal logs on success, actionable logs on failure
- [ ] Deterministic test runs

**Workflow**
- [ ] Write acceptance criteria first
- [ ] Add tests before or alongside changes
- [ ] Keep changes small and composable
- [ ] Prefer modules with narrow interfaces

**Context hygiene**
- [ ] Don't paste huge logs/diffs unless necessary
- [ ] Provide targeted file paths and goals
- [ ] Use `devdocs/` for durable plan/progress

**Quality controls**
- [ ] Linter + formatter + CI gate
- [ ] Golden master approach for risky migrations
- [ ] Periodic refactor phases to reduce drift

---

## Closing

"Vibe Engineering" becomes real when you treat agents as part of a system: a loop with tools, constraints, and feedback. If you invest in the harness and make "done" machine-checkable, you can delegate more safely, move faster, and spend more time on the engineering decisions that actually matter.
