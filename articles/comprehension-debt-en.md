# Comprehension Debt: The Real Bottleneck in Agentic Software Delivery
**Version 1.0** | 2026-02-03
### How to engineer reviewability when generation is cheap

## Abstract
Modern coding agents can produce plausible implementations quickly, often reaching “looks done” in minutes. The constraint has shifted: engineering teams are no longer limited by generating code, but by verifying correctness, preserving shared understanding, and integrating changes safely into systems with real invariants.

This article defines **comprehension debt**: the gap between what you shipped and what the team can explain, debug, and operate. It describes the failure modes that drive it—**assumption propagation**, **abstraction bloat**, **dead code accumulation**, and **sycophantic agreement**—and shows why they appear *after* the first draft, when changes start interacting with production reality.

Instead of “prompting better,” the article proposes a practical operating model: treat review as a pipeline with explicit budgets (diff size, scope), require evidence bundles (commands run + outputs + risk notes), enforce deletion and simplification, and use fresh-context reviews to surface conceptual errors early. The goal is to keep agentic velocity **without** turning code review into rubber-stamping.

## What this article focuses on
This article focuses on:

- team-level constraints that keep PRs reviewable
- verification evidence and review checklists
- process patterns that reduce conceptual failures

It intentionally does *not* re-teach:

- harness setup and “one-command validation” (see *Vibe Engineering 101*)
- spec templates and requirement structure (see *Spec-Driven Development*)
- context management basics (see *Claude Code 101* / *How to Master Claude Code*)

## Article map
If you’re short on time, start with sections **4–7**. They contain the concrete practices that make agentic delivery scale *without* rubber-stamping.

1. **The new constraint**: from writing code to proving correctness
2. **Comprehension debt**: definition, leading indicators, and why it compounds
3. **Four failure modes**: conceptual mistakes agents make (and why they persist)
4. **Reviewability engineering**: diff budgets, scope rules, and deletion bias
5. **Evidence bundles**: the artifact that makes review scalable
6. **Fresh-context review**: catch conceptual errors with clean inputs
7. **Team policy set**: copy/paste guardrails
8. **What to measure**: signals verification is becoming your bottleneck

---

## 1) The new constraint: from “writing code” to “proving correctness”
Agentic coding changes what is scarce.

When generation is cheap, teams stop being constrained by keystrokes. Instead, the bottleneck becomes **verification**: proving that a change is correct, safe to integrate, and understandable enough to operate later. Addy Osmani calls this the “80% problem”: agents can often get you to a plausible first draft quickly, but the last stretch is dominated by integration reality and human review bandwidth. ([addyo.substack.com](https://addyo.substack.com/p/the-80-problem-in-agentic-coding?utm_source=tldrdev))

### The “last 20%” is not linear
That last part tends to include work that is hard to fully delegate because it depends on system-specific invariants:

- **Edge cases**: rare inputs, concurrency, partial failures, time zones, permissions, data migration quirks
- **Integration correctness**: cross-module contracts, backwards compatibility, rollout constraints
- **Operational safety**: logging, metrics, alerts, debugging paths, rollback plans
- **Performance & cost**: the “it works” draft that is too slow or too expensive
- **Security & compliance**: assumptions about authz/authn, data handling, threat surface

If your process doesn’t make these checks cheap and repeatable, you end up with a paradox: **more code produced, same (or worse) throughput shipped**.

### The practical implication
In agentic delivery, “reviewability” is not a nicety. It is an engineering requirement.

Your system needs a way to answer, for every PR:

- What changed (behaviorally)?
- What evidence says it works?
- What might break, and how would we know?
- What is the rollback story if reality disagrees?

When you can’t answer those quickly, you haven’t shipped code. You’ve shipped **uncertainty**.

---

## 2) Comprehension debt: definition, leading indicators, and why it compounds
**Comprehension debt** is the gap between what you shipped and what the team can explain, debug, and operate confidently later.

It is related to (but different from) technical debt:

- **Technical debt**: “we understand it, but it’s ugly/fragile/slow and we’ll pay later.”
- **Comprehension debt**: “we shipped it, but we can’t really explain it — we’re betting future time on hope.”

### Why it compounds
Comprehension debt grows faster than linearly because each unclear change reduces your ability to validate the next change.

When you don’t fully understand a module, you:

- write weaker tests (you don’t know what to assert)
- miss invariants (“this must always be true”)
- accept brittle abstractions (“it seems reasonable”)
- review by vibes instead of evidence (“LGTM” becomes a coping mechanism)

Over time, review turns into rubber-stamping: your ability to **discriminate** good code from plausible code fails to keep up with the agent’s ability to **generate** plausible code. Osmani highlights this as the hidden cost of the productivity narrative. ([addyo.substack.com](https://addyo.substack.com/p/the-80-problem-in-agentic-coding?utm_source=tldrdev))

### Leading indicators (early warning signs)
If several of these are true, comprehension debt is already accumulating:

- PRs merge with comments like “seems fine” but without concrete verification evidence
- PR summaries describe *what files changed* but not *what behavior changed*
- reviewers ask “why is this needed?” *after* code is written (intent wasn’t anchored)
- diffs routinely include “drive-by” refactors, renames, and new abstractions
- “temporary” code stays forever (feature flags, commented-out blocks, alternative paths)
- the on-call engineer can’t answer “what changed recently?” within a few minutes

The fix is rarely “be more careful.” It’s almost always “engineer the workflow so it’s hard to ship unknowns.”

---

## 3) Four failure modes to design against
As Osmani notes, many agent mistakes have shifted from obvious syntax errors to **conceptual failures**: the kind that look coherent in a diff but violate real constraints later. ([addyo.substack.com](https://addyo.substack.com/p/the-80-problem-in-agentic-coding?utm_source=tldrdev))

### 3.1 Assumption propagation
**What it is:** the agent makes an early assumption (“this API behaves like X”, “this field is always present”) and builds a coherent solution on top of it.

**How it shows up:**

- a refactor changes meaning subtly (e.g., timezone handling, nullability, casing, auth checks)
- new logic mirrors a pattern that is *almost* right but violates a local invariant
- tests pass because they don’t cover the real production shape

**Countermeasures:**

- Require an explicit **Assumptions** list in the PR evidence bundle.
- Add a “prove it” check: tests for edge cases, contract tests, or a quick integration run.
- Do a short “explore first” step: find the existing pattern in the codebase before implementing.

### 3.2 Abstraction bloat
**What it is:** the agent introduces unnecessary layers (factories, managers, generic frameworks) that increase surface area and reduce clarity.

**How it shows up:**

- a 20-line behavior change becomes 5 files and a new “architecture”
- abstractions that are not reused (yet) but demand everyone learn them now
- “flexibility” that’s never required, traded for immediate complexity

**Countermeasures:**

- Default rule: **no new abstraction without a concrete reuse case**.
- Prefer the simplest correct implementation, then extract only if repetition appears.
- Enforce **diff budgets** so bloat can’t hide in a “big but plausible” PR.

### 3.3 Dead code accumulation
**What it is:** old implementations linger, alternate paths stay reachable, and “temporary” scaffolding becomes permanent.

**How it shows up:**

- duplicated functions (“v1” and “v2”) both exist “just in case”
- feature flags with no removal plan
- large diffs that add new behavior but don’t delete the old behavior

**Countermeasures:**

- Bias toward **deletion**: if you add a new path, delete the old path in the same PR (or in an explicitly scheduled follow-up).
- Treat commented-out code as a smell: delete it, rely on git history.
- Add static checks where possible (unused exports, unreachable code, coverage drops).

### 3.4 Sycophantic agreement
**What it is:** the agent confidently agrees and executes, even when requirements conflict, are underspecified, or imply tradeoffs.

**How it shows up:**

- “sure!” implementations that ignore non-goals or hidden priorities
- changes that “work” but shift product behavior in unintended ways
- missing tradeoff discussion (speed vs correctness, caching vs staleness, etc.)

**Countermeasures:**

- Make tradeoffs explicit in the spec or PR: “we optimize for X over Y.”
- Require a “Risks & tradeoffs” section in the evidence bundle.
- Use **fresh-context review** (section 6) to force critique, not continuation.

---

## 4) Reviewability engineering: diff budgets, scope rules, and deletion bias
If review is your bottleneck, you can’t “fix it” with more prompting. You fix it by designing work so it is reviewable by default.

### Diff budgets (make PRs readable in one sitting)
Pick budgets that fit your team, but make them explicit. Example starting points:

- **One behavior change per PR** (everything else is a follow-up PR)
- **Cap blast radius**: 1 subsystem, 1 public interface, or 1 user-facing flow
- **Cap size**: e.g. 200–400 LOC net change, ≤10 files (tune to your reality)
- **Cap novelty**: no brand-new “framework” + behavior change in the same PR

The right budget is the one your reviewers can handle without context collapse. If review routinely takes days, the PRs are too big.

### Split refactors from behavior changes
Agents are great at “cleaning up,” but cleanup is expensive to verify when mixed with behavior changes.

Two pragmatic rules:

- If it changes behavior, it must have focused verification (tests/evidence).
- If it’s “just refactor,” it should be mechanically verifiable (no logic changes) and land separately.

### Deletion bias (fight entropy)
When generation is cheap, systems bloat unless you actively delete.

In reviews, ask:

- What did we remove?
- What got simpler?
- What old path no longer needs to exist?

If a PR only adds, month after month, comprehension debt is almost guaranteed.

---

## 5) Evidence bundles: make verification cheap and reusable
An **evidence bundle** is a small, standardized artifact that travels with the PR. It answers “why should I believe this?” without requiring the reviewer to replay the entire agent session.

Done right, it becomes the first thing a reviewer reads and the last thing you need when debugging a regression.

### Minimal evidence bundle template (copy/paste)
Use this in PR descriptions or as a required checklist.

```md
## Evidence bundle
- Goal:
- Non-goals:
- Behavior change (1–3 bullets):
  - ...
- How verified:
  - `command` (result)
  - `command` (result)
- Risks / edge cases:
  - ...
- Rollout / rollback:
  - ...
- Assumptions:
  - ...
```

### Why it works
Evidence bundles reduce comprehension debt because they:

- force explicit intent (goal/non-goals)
- turn “trust me” into “here’s what I ran”
- surface assumptions early (before they become architecture)
- make review less dependent on who generated the code

---

## 6) Fresh-context review patterns
Long agent sessions create a new problem: reviewers can’t (and shouldn’t) read the entire history. The solution is to review in a **fresh context**: treat the diff + evidence as the input, not the conversation.

### Human: evidence-first checklist
Before you get lost in implementation details, check the fundamentals:

- Does this PR do **one** thing?
- Is the behavior change stated clearly (not just “refactored X”)?
- Is there verification evidence (tests/commands/output)?
- Are assumptions and risks called out?
- Did we add complexity that we don’t immediately need?
- Could a teammate explain this change tomorrow without the agent chat?

### Agent: “review from scratch” prompt
Ask an agent to review as if it had no prior context. Provide only the evidence bundle + diff.

```text
You are reviewing a PR. Only use the evidence bundle and diff below.

Return:
1) Summary of the behavior change (max 5 bullets)
2) Assumptions that must be true
3) Risks / edge cases / missing tests
4) Unnecessary complexity (what can be deleted or simplified)
5) Go/No-Go and what would change it
```

This pattern is specifically useful for catching conceptual failures (section 3) because it forces critique instead of continuation.

---

## 7) A lightweight team policy set (copy/paste)
If you want agentic velocity without review collapse, adopt a tiny policy set and enforce it consistently.

```md
## PR reviewability policy (agentic work)
- One behavior change per PR.
- Diff budget: keep PRs reviewable in one sitting (set team numbers for LOC/files/subsystems).
- Evidence bundle required for all behavior changes.
- Refactors and behavior changes land separately.
- No new abstraction layer without a concrete reuse case.
- Delete dead code (no “temporary” branches without a removal plan).
- Fresh-context review required when:
  - the change is high-risk (auth, money, permissions, data migrations)
  - the diff exceeds budget
  - the reviewer can’t explain the change after reading the PR once
```

You can paste this into a repo handbook, a PR template, or even your `agents.md` as a shared constraint.

---

## 8) What to measure: signals verification is becoming your bottleneck
If you only measure “PRs merged,” agentic work will look great right until it collapses.

Measure the verification system.

### Review load signals

- median PR size (files touched, LOC, “net change”)
- median time-to-first-review and time-to-merge
- number of review rounds (comment cycles) per PR
- percentage of PRs missing evidence bundles (should trend to ~0)

### Quality/operations signals

- revert rate within 24–72 hours of merge
- incidents linked to “recent change we didn’t fully understand”
- time-to-diagnose regressions (if it’s rising, comprehension debt is rising)

### Comprehension signals (harder, but valuable)

- random “explain this PR” spot checks in review (can the author do it in 2 minutes?)
- onboarding time to become effective in the codebase
- “fear-of-touching” areas (modules everyone avoids)

When these trend the wrong way, the fix is almost always the same: smaller diffs, stronger evidence, fewer assumptions, and more deletion.

## References
- Addy Osmani — “The 80% Problem in Agentic Coding” ([addyo.substack.com](https://addyo.substack.com/p/the-80-problem-in-agentic-coding?utm_source=tldrdev))

