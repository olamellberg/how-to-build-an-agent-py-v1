# Spec-Driven Development: Practical Guide
**Version 1.2** | 2026-01-29
### A practical guide to building from clear specs

## 1) Introduction: the problem SDD solves

Spec work often fails in two ways: it is either too vague to guide implementation, or too heavy to be used consistently. In AI-assisted development, this gets worse as context grows, assumptions drift, and small errors compound.

SDD exists to keep intent stable while execution iterates. It creates a shared target, tightens the feedback loop, and makes “done” testable.

---

## 2) What SDD is (and is not)

**Spec-Driven Development (SDD)** means you define the intended behavior before you implement it. The spec anchors decisions, scope, and validation.

SDD is **not** enterprise theater. It is a lightweight way to remove ambiguity and make “done” verifiable.

---

## 3) Why SDD matters right now (context rot)

As AI sessions grow, quality often degrades. Context gets noisy, assumptions drift, and small mistakes compound. A spec is the antidote: it keeps the target stable while the model iterates.

SDD makes agentic work safer because:
- requirements are explicit
- constraints are visible
- validation is defined up front
- the loop can self-correct without guesswork

---

## 4) The SDD lifecycle (discover → plan → execute → verify)

SDD is a loop, not a document.

1) **Discover:** clarify the real problem, constraints, and non-goals  
2) **Plan:** turn intent into testable requirements and interfaces  
3) **Execute:** implement in small, reviewable steps  
4) **Verify:** check against tests/evals and tighten the spec

Keeping the lifecycle explicit prevents drift and keeps context fresh.

One practical warning: the cost of verification is often **non-linear**. The first draft can be cheap; the “last 20%” (integration invariants, edge cases, rollout/rollback, observability) is where teams lose time. Make verification explicit early so you don’t discover hidden work at the end.

---

## 5) The Minimum Viable Spec (MVS)

A useful spec can be short. The minimum that works:

- **Goal:** what outcome are we aiming for?
- **Success criteria:** what proves it's done?
- **Constraints:** boundaries, non-goals, invariants
- **Inputs/outputs:** format, schema, interfaces
- **Examples:** one good, one bad
- **Validation:** tests or checks to run
- **Assumptions & unknowns:** what must be true for this to work (and what you’re not sure about yet)
- **Rollout/rollback (brownfield):** how to ship safely and how to back out if reality disagrees

If these six items are clear, implementation becomes straightforward.

---

## 6) Spec structure that scales

As systems grow, specs need a consistent shape:

1) **Context:** current state and constraints  
2) **Problem:** what needs to change  
3) **Requirements:** must/should/won’t  
4) **Interface:** APIs, inputs/outputs, formats  
5) **Validation:** tests, checks, or evals  

This keeps specs short but complete and makes review easier.

---

## 7) Make requirements testable

Write requirements that can be verified:
- “Must return JSON with fields X, Y, Z”
- “Must pass `npm test`”
- “Must not change public API”

Use **Must / Should / Won’t** to avoid scope creep and make priorities explicit.

---

## 8) Specs as executable checks

In agentic work, **tests and evals are executable specs**. If a requirement cannot be tested, it is easy to ignore. If it is encoded in checks, the loop enforces it automatically.

Rule of thumb: every important constraint should have a concrete check.

---

## 9) Keep context fresh with small, staged work

Quality drops when tasks are too big. Break work into small, atomic steps with clear verification. This reduces context bloat and makes the feedback loop reliable.

Signals you are too big:
- multiple unrelated files changed at once
- long, ambiguous prompts
- validation steps are unclear or missing
- the diff is too large to review “in one sitting” (your review bandwidth is the bottleneck)

---

## 10) Greenfield vs brownfield specs

**Greenfield:** focus on vision, boundaries, and non-goals to avoid over-building.  
**Brownfield:** focus on compatibility, invariants, and regression checks.

The same spec structure works, but the emphasis shifts.

---

## 11) Minimal spec template

```md
# Spec: <feature name>

## Goal
<What outcome are we aiming for?>

## Success criteria
- ...
- ...

## Constraints / Non-goals
- ...

## Inputs / Outputs
- Input:
- Output:
- Format:

## Requirements (Must / Should / Won’t)
Must:
- ...

Should:
- ...

Won’t:
- ...

## Validation
- Tests:
- Commands:
```

Use this template as a starting point and keep it short. The spec should reduce ambiguity, not create a new project.

---

## 12) GSD as a simple way to get started

If you want a low-friction way to practice SDD, GSD is a solid option right now. It provides a lightweight workflow with clear stages (ask → plan → execute → verify) and keeps specs and validation close to the work.

You don’t need to adopt the whole system to benefit. Use it as a starting point, then adapt the process to your team and constraints.
