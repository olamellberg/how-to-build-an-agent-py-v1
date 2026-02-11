# VSCode + Codex Local: From Zero to Agentic Development
**Version 1.0** | 2026-02

A practical hands-on guide for developers who want to get started with OpenAI Codex in VSCode.

## Why Codex Local now

Codex Local enables agentic development directly in your editor and your own repository. You get local execution, sandboxed commands, and fast iteration without leaving your workflow.

## Installation and setup

1. Install the Codex extension in VSCode.
2. Sign in with your ChatGPT account.
3. Open a project in a local workspace.
4. Validate setup with a simple prompt, for example: "Describe the project structure in this folder."

## AGENTS.md and guidance

Create an `AGENTS.md` file in the repo root to provide clear rules:
- which commands should run
- coding standards and architectural boundaries
- what must not change

This reduces unnecessary diffs and improves consistency.

## Practical workflow

A good starter flow:
1. Define the target state with clear acceptance criteria.
2. Reference relevant files with `@filename`.
3. Ask the agent for a plan before full implementation.
4. Review diff, run tests, and iterate in small steps.

## Common pitfalls

- Prompts that are too broad often create oversized and unclear changes.
- Missing `AGENTS.md` increases implicit assumptions from the agent.
- Missing tests make it hard to verify if the output is actually correct.

## Summary

VSCode + Codex Local is a strong fit for teams that want to increase delivery speed without losing control. The key is clear instructions, small verifiable steps, and disciplined testing and review.
