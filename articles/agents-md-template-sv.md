# agents.md / CLAUDE.md Mall
### En kopiera-klistra-mall konsekvent med handbokens vägledning

Denna sida innehåller en minimal, repo-specifik mall för `agents.md` eller `CLAUDE.md`. Mallen är designad för att vara konsekvent med vägledningen i [Agents.md Explained](agents-md-explained.html) och [Claude Code 101](claude-code-101.html).

---

## Tom mall (kopiera och anpassa)

```markdown
# agents.md

## Commands
- Build: <kommando>
- Test: <kommando>
- Lint: <kommando>
- Format: <kommando>

## Structure
- <katalog>: <beskrivning>
- <katalog>: <beskrivning>

## Stack
- <teknologi> <version>
- <teknologi> <version>

## Boundaries
- Never <vad som inte får göras>
- Never <vad som inte får göras>

## Working Style
- Start with a plan (3–7 steps)
- After each step: summarize diff + commands run + remaining risks
- If uncertain: stop and ask for a decision
```

---

## Fyllda exempel

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

### Håll den kort
- Fokusera på repo-specifika regler, inte generella förklaringar
- Undvik att förklara vad "komponenter" är — modellen vet redan det

### Förklara "varför"
- "Använd TypeScript strict mode eftersom implicit any orsakade produktionsbuggar"
- Detta hjälper modellen göra bättre bedömningar i kantfall

### Uppdatera kontinuerligt
- Varje gång du korrigerar samma misstag två gånger, lägg till en regel
- Varje fix förhindrar framtida omarbete

### Var specifik
- "Never commit secrets" är bra
- "Never commit secrets, check `.env.example` för format" är bättre

---

## Relaterade artiklar

- [Agents.md Explained](agents-md-explained.html) — djupdykning i agents.md
- [Claude Code 101](claude-code-101.html) — specifikt för CLAUDE.md
- [Repository Harness Setup](repo-harness-setup.html) — hur du sätter upp validering
