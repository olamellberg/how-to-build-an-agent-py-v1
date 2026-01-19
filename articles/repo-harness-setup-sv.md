# Repository Harness Setup
### Checklista för ett-kommando CI, loggsignal och determinism

En **repository harness** är den infrastruktur som gör att en agent kan arbeta pålitligt i ditt repository. Denna guide ger en praktisk checklista för att sätta upp en.

---

## Kärnprincip: Ett kommando för att validera

Ditt projekt bör bygga, testa och lint med **ett enda kommando**.

### Exempel

**Node.js/TypeScript:**
```bash
npm run check  # Kör: build + test + lint
```

**Python:**
```bash
make check  # Kör: pytest + black --check + mypy
```

**C#/.NET:**
```bash
dotnet build && dotnet test && dotnet format --verify
```

**Rust:**
```bash
cargo test && cargo fmt --check && cargo clippy
```

### Varför det spelar roll

Om validering kräver "tribal knowledge" ("exportera denna variabel", "kör detta i den mappen", "installera detta systemberoende manuellt"), kommer din agent-loop att slösa kontext och tid på att återupptäcka det — om och om igen.

---

## Checklista: Grundläggande setup

### [ ] Ett-kommando-validering

- [ ] Skapa ett kommando (t.ex. `make check`, `npm run check`, `./scripts/ci.sh`) som kör:
  - [ ] Bygge/kompilering
  - [ ] Tester
  - [ ] Linting
  - [ ] Formatering (validering)
- [ ] Kommandot fungerar i CI och lokalt på samma sätt
- [ ] Kommandot ger tydlig exit-kod (0 = success, != 0 = failure)

### [ ] Deterministiska tester

- [ ] Tester ger samma resultat varje gång (inga race conditions, inga timestamps i assertions)
- [ ] Tester kan köras parallellt utan konflikter
- [ ] Tester är isolerade (inga delade tillstånd mellan tester)

### [ ] Tydlig feedback

- [ ] **Vid framgång:** Minimala loggar (t.ex. "✅ 1000 tester passerade" istället för 1000 rader av "ok")
- [ ] **Vid misslyckande:** Åtgärdbara loggar:
  - [ ] Visar det misslyckade påståendet
  - [ ] Visar relevant diff
  - [ ] Visar minimal stack trace
  - [ ] Visar relevant fil/rad

### [ ] Stabila skript

- [ ] Inga "tribal knowledge"-krav (ingen manuell export av miljövariabler, inga manuella installationer)
- [ ] Skript fungerar i Docker/CI på samma sätt som lokalt
- [ ] Sökvägar är relativa eller via miljövariabler

---

## Exempel: package.json (Node.js)

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

---

## Exempel: Makefile (Python)

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

---

## Exempel: scripts/ci.sh (Bash)

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

---

## Loggfiltering för agenter

Agenter läser all output som feedback. Designa loggarna för en automatiserad medarbetare:

### Bra: Koncis vid framgång
```
✅ 1000 tests passed in 2.3s
```

### Dåligt: Brusig vid framgång
```
test 1: ok
test 2: ok
test 3: ok
... (997 more lines)
```

### Bra: Åtgärdbart vid misslyckande
```
FAIL: src/auth.test.ts:42
Expected: "user@example.com"
Received: "admin@example.com"
```

### Dåligt: Rörigt vid misslyckande
```
[1000 lines of stack trace and compiler output]
```

---

## Determinism

### Problem: Icke-deterministiska tester

```javascript
// Dåligt: använder nuvarande tid
expect(result).toBe(new Date().toISOString());

// Bra: deterministisk
expect(result).toBe("2026-01-14T12:00:00Z");
```

### Problem: Race conditions

```python
# Dåligt: kan misslyckas ibland
def test_concurrent():
    results = []
    threads = [Thread(target=worker) for _ in range(10)]
    # ...

# Bra: isolerat eller explicit synkronisering
def test_concurrent():
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(worker, range(10)))
    # ...
```

---

## Integration med agents.md

Lägg till i din `agents.md`:

```markdown
## Commands
- Validate: make check
- Build: make build
- Test: make test

## Validation
Always run `make check` before committing. If it fails, fix errors and retry.
```

---

## Nästa steg

När din harness är på plats:
1. Testa att en agent kan arbeta i repot utan förvirring
2. Observera vilka mönster som uppstår
3. Justera loggar och feedback baserat på vad agenten behöver

**Relaterade artiklar:**
- [Vibe Engineering 101](vibe-engineering-101.html) — mer om harness-design
- [Agents.md Explained](agents-md-explained.html) — hur agents.md fungerar med harness
