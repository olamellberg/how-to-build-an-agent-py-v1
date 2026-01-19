# Repository Harness Setup
### Checklist for one-command CI, log signal, and determinism

A **repository harness** is the infrastructure that makes an agent work reliably in your repository. This guide provides a practical checklist for setting one up.

---

## Core Principle: One Command to Validate

Your project should build, test, and lint with **a single command**.

### Examples

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

### Why It Matters

If validation requires "tribal knowledge" ("export this variable", "run this in that directory", "install this system dependency manually"), your agent loop will waste context and time re-discovering it — over and over.

---

## Checklist: Basic Setup

### [ ] One-Command Validation

- [ ] Create a command (e.g., `make check`, `npm run check`, `./scripts/ci.sh`) that runs:
  - [ ] Build/compilation
  - [ ] Tests
  - [ ] Linting
  - [ ] Formatting (validation)
- [ ] Command works the same in CI and locally
- [ ] Command provides clear exit code (0 = success, != 0 = failure)

### [ ] Deterministic Tests

- [ ] Tests give the same results every time (no race conditions, no timestamps in assertions)
- [ ] Tests can run in parallel without conflicts
- [ ] Tests are isolated (no shared state between tests)

### [ ] Clear Feedback

- [ ] **On success:** Minimal logs (e.g., "✅ 1000 tests passed" instead of 1000 lines of "ok")
- [ ] **On failure:** Actionable logs:
  - [ ] Shows the failing assertion
  - [ ] Shows relevant diff
  - [ ] Shows minimal stack trace
  - [ ] Shows relevant file/line

### [ ] Stable Scripts

- [ ] No "tribal knowledge" requirements (no manual export of environment variables, no manual installations)
- [ ] Scripts work in Docker/CI the same way as locally
- [ ] Paths are relative or via environment variables

---

## Example: package.json (Node.js)

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

## Example: Makefile (Python)

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

## Example: scripts/ci.sh (Bash)

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

## Log Filtering for Agents

Agents read all output as feedback. Design logs for an automated collaborator:

### Good: Concise on Success
```
✅ 1000 tests passed in 2.3s
```

### Bad: Noisy on Success
```
test 1: ok
test 2: ok
test 3: ok
... (997 more lines)
```

### Good: Actionable on Failure
```
FAIL: src/auth.test.ts:42
Expected: "user@example.com"
Received: "admin@example.com"
```

### Bad: Messy on Failure
```
[1000 lines of stack trace and compiler output]
```

---

## Determinism

### Problem: Non-Deterministic Tests

```javascript
// Bad: uses current time
expect(result).toBe(new Date().toISOString());

// Good: deterministic
expect(result).toBe("2026-01-14T12:00:00Z");
```

### Problem: Race Conditions

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

---

## Integration with agents.md

Add to your `agents.md`:

```markdown
## Commands
- Validate: make check
- Build: make build
- Test: make test

## Validation
Always run `make check` before committing. If it fails, fix errors and retry.
```

---

## Next Steps

When your harness is in place:
1. Test that an agent can work in the repo without confusion
2. Observe what patterns emerge
3. Adjust logs and feedback based on what the agent needs

**Related articles:**
- [Vibe Engineering 101](vibe-engineering-101.html) — more on harness design
- [Agents.md Explained](agents-md-explained.html) — how agents.md works with harness
