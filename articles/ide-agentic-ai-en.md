# Agentic AI in the IDE for .NET backend and JavaScript frontend
**Version 1.0** | 2026-01-22

Agentic AI in an IDE is more than "autocomplete". It's a workflow where the assistant can **plan**, propose **multi-file diffs**, run **build/test/lint**, read failures, and iterate toward clear acceptance criteria. For the general methodology (harness, feedback loops, context hygiene), refer to your existing articles on agent loops and "model CI".

This article focuses on what is **IDE-specific**: which IDEs/editors are relevant without JetBrains, what model families they typically expose, how agentic workflows look in real engineering for .NET + JS, and what it costs (indicative).

---

## 1) What you're actually choosing when you pick "IDE + agent"
In practice you are choosing four things at once:

1) **Context engine**: how the editor/agent gathers relevant files and diffs.  
2) **Agent capabilities**: plan mode, multi-file edits, command execution, PR support.  
3) **Model portfolio**: which model families (OpenAI/Anthropic/Google, etc.) you can select for different tasks. GitHub Copilot publishes an official list of supported models for Copilot Chat.  
4) **Governance/cost**: licenses, usage/premium requests, team policies.

---

## 2) Compact matrix: IDE ↔ models ↔ agent capability ↔ price

> **Price** = list price in USD (excl. VAT), indicative. Features and model availability vary by plan and may change over time.

| IDE / editor | AI assistants (examples) | Model families & vendors (examples) | Agentic support (practical) | Indicative price |
|---|---|---|---|---|
| **VS Code** | GitHub Copilot • Gemini Code Assist • Amazon Q Developer • (optional BYOK via Continue) | Copilot: model selection in Copilot Chat across multiple vendors. • Gemini Code Assist: Google (Gemini). • Amazon Q Developer: AWS service for agentic coding assistance. | Multi-file diffs, plan/agent modes (plan-dependent), and the loop "edit → run checks → iterate". | Copilot Pro **$10/mo**, Pro+ **$39/mo**. • Amazon Q Developer Pro: **$19/user/mo** (list price). • Gemini Code Assist: Standard/Enterprise via Google Cloud pricing. |
| **Visual Studio** | GitHub Copilot | Copilot models per GitHub. | Agentic chat/edit in the IDE; a strong fit for .NET "vertical slices" (API + tests) when you have a repo harness. | Copilot licensing per GitHub: Business **$19/user/mo** (org) plus individual Pro/Pro+ above. |
| **Cursor** | Cursor (built-in agents + team controls) | Model costs and governance are documented in Cursor pricing (usage-based, per model). | AI-native agentic workflow: multi-file edits, agent runs, and team-level spend controls. | Teams: spend controls and model pricing via Cursor. |
| **Windsurf** | Windsurf (Cascade) | Model catalog / premium models are determined by Windsurf plan and credits. | AI-native agent flow via Cascade (multi-step in the editor). | Windsurf pricing (plans for individuals/teams/enterprise). |
| **Claude Code** (Terminal) | Claude Code CLI | Anthropic (Claude Opus 4.5, Sonnet 4, Haiku). Direct API access, no intermediary. | Full agentic CLI: multi-file edits, bash execution, git operations, plan mode, sub-agents. Works in any terminal alongside your IDE. | Anthropic API pricing (usage-based). Pro plan includes Claude Code usage. |

**How to read this for .NET + JS teams:**
- If you want an "enterprise-default" that's easy to standardize in the Microsoft ecosystem: **VS Code/Visual Studio + Copilot** is typically the most predictable rollout path (licensing and docs are very explicit).
- If you want a Google-first IDE assistant: **Gemini Code Assist** is Google's primary IDE offering.
- If you want an AI-first editor with a stronger agent experience: **Cursor/Windsurf** often push agent workflows further, but also become a platform you need to standardize and cost-control.
- If you want maximum agentic power without changing IDE: **Claude Code** runs in your terminal alongside any editor. It offers the most capable agentic loop (plan mode, sub-agents, full bash access) with direct Anthropic API access.

---

## 3) Practical starting bundles for teams
These three "baseline" bundles usually work without creating tool chaos:

### Bundle A: Microsoft standard (most compatible)
- **VS Code for JS/TS and polyglot**
- **Visual Studio for .NET** (when it adds value in debugging/profiling)
- **GitHub Copilot** as the shared AI baseline

This makes it easier to establish consistent guidance for model selection, prompts, and workflows (because Copilot concepts are consistent across both IDEs).

### Bundle B: Google-first IDE assistant
- **VS Code**
- **Gemini Code Assist** (Standard/Enterprise when you need org-level features)

Gemini Code Assist is available as "for individuals" and in Standard/Enterprise tiers, documented via Google Developer/Cloud docs.

### Bundle C: AI-first editor
- **Cursor** or **Windsurf** for teams that want to push agentic workflows further inside the editor
- Clear spend-control processes to avoid cost surprises (Cursor documents spend controls for Teams).

### Bundle D: Terminal-first agentic (Claude Code)
- **Any IDE you already use** (VS Code, Visual Studio, Vim, etc.)
- **Claude Code** running in a terminal pane or separate window
- Best for developers who want the strongest agentic capabilities without switching editors
- Claude Code reads `CLAUDE.md` (similar to `agents.md`) for repo context, runs bash commands, creates PRs, and can spawn sub-agents for parallel work
- Combines well with lightweight IDE extensions (Copilot for autocomplete, Claude Code for heavy agentic tasks)

---

## 4) Agentic workflows in the IDE (compressed, with references)
Rather than repeating fundamentals from your earlier articles, this section provides an **IDE-oriented checklist** you can copy into a team working agreement.

### 4.1 Standard loop: "Plan → Diff → Check → Iterate"
- A **single validation signal** (e.g., `make check` or `./scripts/ci.sh`) is the highest-leverage accelerator for agentic development.  
- Agentic work scales when you can trust the loop (agent changes code, runs checks, iterates until green, then presents diff + risks).  
- For the complete methodology (harness design, context as "RAM", log signal): see *Vibe Engineering 101*.  

### 4.2 .NET: "Vertical slice" as the default unit of work
Run the agent on tasks with clear steps and clear verification:
- Endpoint + domain rule + persistence + tests (and optionally swagger/contract)
- Small diffs (max 3–7 files per iteration)
- `dotnet build` + `dotnet test` after each batch

This fits the "tool-driven, easy to validate" category where agent loops typically produce the best results.  

### 4.3 JS/TS: "Feature + states + test"
Have the agent work around:
- UI states (loading/error/success)
- explicit error handling (409/400/500)
- lint/test/build as the gate

Keep logs minimal and targeted—overloaded context reduces precision.  

### 4.4 Reset rule when the session degrades
When the agent starts looping, it's often faster to reset than to rescue a noisy context. Your `/compact` → `/clear` routine and re-injecting plan + constraints + current errors is a solid default.  

---

## 5) Protecting sensitive code and information (consolidated)

This section is the operational, short version. For the broader principles (why stable context and repo "contracts" such as agents.md matter), see *Agents.md Explained*.

### 5.1 Minimize the data surface that can leave the machine
- Maintain an **AI allowlist** of folders the agent may read (e.g., `/src`, `/tests`) and a **denylist** for everything that must never enter context (`/secrets`, certs, prod-config, customer exports).
- Restrict auto-indexing / project scanning in sensitive repos if the tool supports it (goal: the agent only sees what the task requires).

### 5.2 Control tools and network capabilities
- Run commands through a **controlled harness** (script/Makefile) rather than arbitrary execution.
- Whitelist commands (build/test/lint) and require human approval for risk areas (auth, crypto, infra, licenses, secrets).

### 5.3 Stabilize behavior with a repo contract (agents.md)
Keep `agents.md` (or equivalent) short and always include:
- Commands (build/test/lint)
- Structure (key folders)
- Boundaries (what the agent must not do)

This reduces variance across sessions and eliminates recurring failure modes.  

### 5.4 Ops requirement: log tool outcomes and run evals
For production-grade agentic workflows (even internally), treat the model as a pipeline component: tools produce truth, the model proposes changes, and you measure behavior with evals. *AI Fundamentals 2026* describes the minimum bar (pipeline + evals).  

---

## 6) Pricing and licensing notes (for budgeting)
- **Copilot**: individual licenses (Pro/Pro+) and org licenses (Business, etc.) are specified by GitHub.  
- **Amazon Q Developer**: AWS lists pricing and limits for free/pro.  
- **Gemini Code Assist**: pricing and editions (Standard/Enterprise) are documented in Google Cloud.  
- **Cursor**: usage-based (model pricing + token fees + team spend controls).  
- **Windsurf**: plan split is documented on the pricing page.  

---

## 7) A one-week team playbook (Week 1)
1) Introduce **one validation command** (`make check` or `./scripts/ci.sh`) and make it the agent's default tool.  
2) Add `agents.md` with commands/structure/boundaries (keep it compact).  
3) Standardize prompts: **Goal → Constraints/non-goals → Done → Plan first** (your "prompt as engineering communication" pattern).  
4) Establish a reset rule: if the loop degrades → compact/clear and restart clean.  
5) For sensitive repos: enable denylist and restrict tools per 5.1–5.2.
