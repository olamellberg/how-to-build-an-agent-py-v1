# agents.md / CLAUDE.md Template
**Version 1.0** | 2026-01-22
### A copy-paste template consistent with handbook guidance

This page contains a minimal, repo-specific template for `agents.md` or `CLAUDE.md`. The template is designed to be consistent with guidance in [Agents.md Explained](agents-md-explained.html) and [Claude Code 101](claude-code-101.html).

---

## Empty Template (copy and customize)

```markdown
# agents.md

## Commands
- Build: <command>
- Test: <command>
- Lint: <command>
- Format: <command>

## Structure
- <directory>: <description>
- <directory>: <description>

## Stack
- <technology> <version>
- <technology> <version>

## Boundaries
- Never <what not to do>
- Never <what not to do>

## Working Style
- Start with a plan (3–7 steps)
- After each step: summarize diff + commands run + remaining risks
- If uncertain: stop and ask for a decision
```

---

## Filled Examples

### Node.js / TypeScript

```markdown
# agents.md

## Commands
- Build: `npm run build`
- Test: `npm test`
- Lint: `npm run lint`
- Format: `npm run format`
- Validate: `npm run check` (build + test + lint)

## Structure
- `src/`: application code
- `tests/`: test files
- `scripts/`: build and utility scripts

## Stack
- Node.js 20
- TypeScript 5.x
- Jest for testing
- ESLint for linting

## Boundaries
- Never commit secrets or API keys
- Never delete failing tests
- Never modify `package-lock.json` manually
- Never change test expectations to make tests pass

## Working Style
- Start with a plan (3–7 steps)
- After each step: summarize diff + commands run + remaining risks
- If uncertain: stop and ask for a decision
- Always run `npm run check` before committing
```

---

### Python

```markdown
# agents.md

## Commands
- Build: `python -m build`
- Test: `pytest`
- Lint: `ruff check .`
- Format: `black --check .`
- Validate: `make check` (build + test + lint + format)

## Structure
- `src/`: source code
- `tests/`: test files
- `scripts/`: utility scripts

## Stack
- Python 3.11+
- pytest for testing
- ruff for linting
- black for formatting

## Boundaries
- Never commit `.env` files
- Never delete failing tests
- Never modify `requirements.txt` without explicit request
- Never change test expectations to make tests pass

## Working Style
- Start with a plan (3–7 steps)
- After each step: summarize diff + commands run + remaining risks
- If uncertain: stop and ask for a decision
- Always run `make check` before committing
```

---

### C# / .NET

```markdown
# agents.md

## Commands
- Build: `dotnet build`
- Test: `dotnet test`
- Format: `dotnet format --verify`
- Validate: `dotnet build && dotnet test && dotnet format --verify`

## Structure
- `src/`: source projects
- `tests/`: test projects
- `scripts/`: utility scripts

## Stack
- .NET 8
- xUnit for testing
- StyleCop for linting

## Boundaries
- Never commit `appsettings.Development.json` with secrets
- Never delete failing tests
- Never modify `.csproj` files without explicit request
- Never change test expectations to make tests pass

## Working Style
- Start with a plan (3–7 steps)
- After each step: summarize diff + commands run + remaining risks
- If uncertain: stop and ask for a decision
- Always run validation command before committing
```

---

## Best Practices

### Keep It Short
- Focus on repo-specific rules, not general explanations
- Avoid explaining what "components" are — the model already knows

### Explain "Why"
- "Use TypeScript strict mode because implicit any caused production bugs"
- This helps the model make better judgment calls in edge cases

### Update Continuously
- Every time you correct the same mistake twice, add a rule
- Each fix prevents future rework

### Be Specific
- "Never commit secrets" is good
- "Never commit secrets, check `.env.example` for format" is better

---

## Related Articles

- [Agents.md Explained](agents-md-explained.html) — deep dive into agents.md
- [Claude Code 101](claude-code-101.html) — specific to CLAUDE.md
- [Vibe Engineering 101](vibe-engineering-101.html) — how to set up validation and harness
