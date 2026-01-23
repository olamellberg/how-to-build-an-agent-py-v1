# Just Ralph-it
**Version 1.0** | 2026-01-22
### Låt AI:n göra jobbet i en oändlig loop

**Credit:** Ralph-metoden är skapad av [Geoffrey Huntley](https://x.com/GeoffreyHuntley). Denna artikel är en kortfattad sammanfattning — för den fullständiga guiden, se [The Ralph Playbook](https://github.com/ghuntley/how-to-ralph-wiggum) på GitHub.

"Ralph Wiggum Technique" är en utvecklingsmetodik där du låter en AI-agent arbeta autonomt i en oändlig loop. Istället för att mikromanagera agenten steg för steg, sätter du upp rätt struktur — och låter sedan agenten köra tills jobbet är klart.

Idén är enkel: **eventual consistency genom iteration**. Agenten kan göra misstag, men med rätt feedback-loop (tester, linters, bygge) korrigerar den sig själv — om och om igen — tills allt fungerar.

---

## Konceptet: Tre faser, en loop

Ralph-metoden följer ett enkelt arbetsflöde:

1. **Definiera krav** — Diskutera med LLM:en vad du vill bygga. Bryt ner i "Jobs to Be Done" (JTBD). Skriv specifikationer i `specs/*.md`.

2. **Planera** — Kör loopen i "planning mode" för att generera en `IMPLEMENTATION_PLAN.md` med prioriterade uppgifter.

3. **Bygg** — Kör loopen i "build mode". Agenten plockar en uppgift från planen, implementerar, kör tester, committar — och börjar om med nästa.

> **Nyckelinsikt:** Varje loop-iteration startar med rent kontextfönster. Agenten läser samma filer varje gång (`PROMPT.md` + `AGENTS.md`), väljer nästa uppgift från planen, och arbetar fokuserat på *en* sak.

---

## Den grundläggande loopen

I sin enklaste form är Ralph bara en bash-loop:

```bash
while :; do cat PROMPT.md | claude ; done
```

Det är allt. Loopen kör agenten, agenten läser prompten, implementerar nästa uppgift, committar, och avslutar. Bash-loopen startar om direkt — med rent minne.

### Exempel: Utökad loop med mode-val

```bash
#!/bin/bash
# Usage: ./loop.sh [plan] [max_iterations]

if [ "$1" = "plan" ]; then
    MODE="plan"
    PROMPT_FILE="PROMPT_plan.md"
else
    MODE="build"
    PROMPT_FILE="PROMPT_build.md"
fi

while true; do
    cat "$PROMPT_FILE" | claude -p \
        --dangerously-skip-permissions \
        --model opus
    
    git push origin "$(git branch --show-current)"
    
    echo "======================== LOOP COMPLETE ========================"
done
```

> **Viktigt: Sandboxning**  
> `--dangerously-skip-permissions` kringgår alla behörighetsfrågor. Kör alltid i en isolerad miljö (Docker, VM, eller liknande) med minimala credentials. "It's not if it gets popped, it's when."

---

## Nyckelprinciper

### 1. Kontext är allt

En LLM har begränsat "arbetsminne" (context window). Ralph maximerar detta genom att:

- **Hålla uppgifter små** — en uppgift per loop-iteration
- **Rensa kontexten** — varje iteration startar från scratch
- **Använda subagenter** — delegera utforskande arbete för att inte förorena huvudkontexten

### 2. Backpressure via verktyg

Agenten styrs av feedback från verkliga verktyg:

- **Tester** — måste passera innan commit
- **Linters/formatters** — automatisk stilkontroll
- **Bygge** — koden måste kompilera

Om något fallerar, itererar agenten tills det fungerar. Detta är "backpressure" — verktyg som trycker tillbaka mot dålig kod.

### 3. Let Ralph Ralph

Lita på att agenten självkorrigerar. Din roll är att:

- **Observera** — se vilka mönster som uppstår, var agenten går fel
- **Justera strukturen** — uppdatera `PROMPT.md` eller `AGENTS.md` när du ser återkommande problem
- **Lita på loopen** — ge agenten tid att självkorrigera

> "Eventual consistency achieved through iteration."

---

## Filstruktur

Ett typiskt Ralph-projekt ser ut så här:

```
project-root/
├── loop.sh                    # Ralph loop-skript
├── PROMPT_build.md            # Instruktioner för build mode
├── PROMPT_plan.md             # Instruktioner för plan mode
├── AGENTS.md                  # Hur man bygger/kör projektet
├── IMPLEMENTATION_PLAN.md     # Prioriterad uppgiftslista
├── specs/                     # Kravspecifikationer
│   ├── feature-1.md
│   └── feature-2.md
└── src/                       # Källkod (genereras av agenten)
```

### PROMPT_build.md (exempel)

```markdown
# Build Mode

Du är en kodredigeringsagent. Din uppgift:

1. Läs IMPLEMENTATION_PLAN.md
2. Välj nästa uppgift (den första som inte är markerad som klar)
3. Implementera uppgiften
4. Kör tester: `npm test`
5. Om tester passerar: commit med beskrivande meddelande
6. Om tester misslyckas: fixa och försök igen

Regler:
- Ändra bara filer som behövs för nuvarande uppgift
- Följ kodstilen i befintlig kod
- Committa ofta, små commits
```

### AGENTS.md (exempel)

```markdown
## Commands
- Build: `npm run build`
- Test: `npm test`
- Lint: `npm run lint`

## Structure
- src/: källkod
- tests/: tester
- specs/: kravspecifikationer

## Stack
- Node.js 20
- TypeScript 5.x
```

---

## Kom igång

1. **Sätt upp projektet:**
   ```bash
   mkdir ralph-project
   cd ralph-project
   git init
   ```

2. **Skapa `PROMPT_build.md` och `AGENTS.md`** (se exempel ovan)

3. **Kör loopen:**
   ```bash
   chmod +x loop.sh
   ./loop.sh build
   ```

4. **Observera och justera:**
   - Se vilka mönster som uppstår
   - Uppdatera `PROMPT_build.md` när du ser återkommande problem
   - Lita på att agenten självkorrigerar

---

## Varför det fungerar

Ralph fungerar eftersom:

1. **Rent minne varje iteration** — agenten ser bara det som behövs
2. **Deterministisk feedback** — tester och bygge ger tydliga signaler
3. **Eventual consistency** — med tillräckligt många iterationer konvergerar systemet mot "klart"
4. **Autonomi** — du behöver inte mikromanagera varje steg

Det är inte perfekt. Det är inte snabbt. Men det är *automatiskt* — och det är kraften.

---

## Referenser

- [The Ralph Playbook](https://github.com/ghuntley/how-to-ralph-wiggum) — komplett guide av Geoffrey Huntley
- [Geoffrey Huntley på X](https://x.com/GeoffreyHuntley)
