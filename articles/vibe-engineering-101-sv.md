# Vibe Engineering 101
**Version 1.0** | 2026-01-22
*En praktisk guide för systemutvecklare som vill komma igång med agentbaserad utveckling*

Agentbaserad utveckling handlar mindre om "AI som skriver kod" och mer om att designa en pålitlig loop: en modell föreslår ändringar, verktyg validerar dem, och återkoppling driver nästa iteration. Den här artikeln är en fältguide för att bygga den loopen så att den producerar användbar mjukvara — konsekvent.

Målet här är inte att romantisera "vibe coding", utan att göra det operationellt: tydliga begränsningar, snabb feedback och repeterbara resultat.

---

## 1) Vad en agent faktiskt är

En användbar arbetsdefinition är:

**En agent kör verktyg i en loop för att uppnå ett mål.**

Ur ett ingenjörsperspektiv är det medvetet oglamoröst. Systemet är typiskt:

1. Ange ett mål + begränsningar  
2. Modellen föreslår åtgärder (redigera filer, köra kommandon, inspektera utdata)  
3. Verktyg körs (tester, linters, byggen, sökning, exekvering)  
4. Resultaten går tillbaka in i loopen  
5. Upprepa tills acceptanskriterierna är uppfyllda

Denna enkelhet är goda nyheter: det betyder att agentbaserade system går att konstruera och förbättra. Du kan förbättra dem genom att förbättra loopen, inte genom att behandla modellen som magi.

---

## 2) Ditt kontextfönster är ditt "RAM"

LLM:er "kommer inte ihåg" ditt repository — när som helst opererar de på tokens du har tillhandahållit (plus vad dina verktyg injicerar). Praktiskt:

- **Allt som spelar roll måste finnas i kontexten** (eller vara pålitligt hämtbart via verktyg).
- **Mer kontext är inte alltid bättre.** Överfulla kontexter ökar förvirring, felaktig verktygsanvändning och subtila fel.
- **Du behöver hantera vad som går in i loopen.**

### Praktiska tumregler
- Undvik att låta verktyg dumpa stora blobbar av loggar, diffar eller hela repos i prompten.
- Håll feedback **minimal och åtgärdbar** (mer om detta i harness-sektionen).
- Om din agent/verktyg auto-injicerar kontext, lär dig vad det inkluderar och hur du ställer in det.

### En användbar mental modell
Behandla kontextfönstret som ont om minne i äldre system. Om du låter det fyllas med brusiga loggar och redundant information, försämras prestandan på samma sätt som en begränsad maskin när den svälter på resurser.

---

## 3) Den stora avkopplingen: skriva kod vs konstruera system

Agentbaserad utveckling förstärker en förskjutning som många utvecklare redan upplever med senioritet:

- **Programmering (skriva kod)** blir billigare.
- **Konstruktion (design, begränsningar, testning, avvägningar)** blir mer värdefullt.

Modeller är ofta mycket starka på:
- syntax och boilerplate
- översätta avsikt till implementation
- generera variationer snabbt
- arbeta över okända ekosystem (med vägledning)

De är fortfarande svaga eller opålitliga på:
- förstå din affärskontext som standard
- göra produktavvägningar utan tydliga prioriteringar
- gissa icke-uppenbara systembegränsningar
- upprätthålla sammanhang över långa, röriga historier

Så rollen ändras: du spenderar mer tid på specs, acceptanskriterier, tester och arkitektur — och mindre tid på tangenttryckningar.

---

## 4) Du är nu Tech Lead + QA Lead

En produktiv ram är:

- **Du definierar "klart".**
- **Du designar feedback-loopen.**
- **Du granskar resultat, inte varje rad.**

Modeller beter sig som extremt snabba medarbetare utan långsiktigt minne. De kan röra sig snabbt, men de behöver:
- tydliga begränsningar
- skarpa definitioner av framgång
- deterministisk feedback (tester, lint, build)
- skyddsräcken mot drift

Detta är kärnfärdigheten: **bygg "model CI" in i ditt arbetsflöde**.

---

## 5) Sluta kämpa mot modellen — bygg en bättre harness

Ett vanligt misslyckande är att behandla modellen som en juniorutvecklare du måste mikrostyra i realtid. Det skapar en mänsklig flaskhals och minskar genomströmning.

I stället för att manuellt fixa formatering, namn eller små stilfrågor:
- koda in regler i verktyg (formatter/linter)
- låt agenten köra verktygen
- använd misslyckanden som feedback-signaler

När agenten går åt fel håll, anta att något av detta är sant:
1. **Planen var under-specad.**
2. **Acceptanskriterierna var vaga.**
3. **Feedback-loopen är svag eller brusig.**

Fixen är sällan "titta hårdare." Det är vanligtvis:
- förbättra specen
- skärpa testerna
- minska brus i utdata
- försök igen rent

---

## 6) Projektupplägg är allt

Den bästa tidsinvesteringen du kan göra är ett repo som en agent kan arbeta i utan förvirring. En **repository harness** är den infrastruktur som gör att en agent kan arbeta pålitligt.

### Hård krav: ett kommando för att validera
Ditt projekt bör bygga, testa och lint med **ett enda kommando**.

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

Om validering kräver stamkunskap ("exportera denna variabel", "kör detta i den mappen", "installera detta systemberoende manuellt"), kommer din loop att slösa kontext och tid på att återupptäcka det — om och om igen.

### Setup-checklista

**Ett-kommando-validering:**
- [ ] Skapa ett kommando (t.ex. `make check`, `npm run check`, `./scripts/ci.sh`) som kör bygge, tester, linting och formatering
- [ ] Kommandot fungerar i CI och lokalt på samma sätt
- [ ] Kommandot ger tydlig exit-kod (0 = success, != 0 = failure)

**Deterministiska tester:**
- [ ] Tester ger samma resultat varje gång (inga race conditions, inga timestamps i assertions)
- [ ] Tester kan köras parallellt utan konflikter
- [ ] Tester är isolerade (inga delade tillstånd mellan tester)

**Tydlig feedback:**
- [ ] Vid framgång: minimala loggar (t.ex. "✅ 1000 tester passerade" istället för 1000 rader av "ok")
- [ ] Vid misslyckande: åtgärdbara loggar som visar det misslyckade påståendet, relevant diff, minimal stack trace, relevant fil/rad

**Stabila skript:**
- [ ] Inga "tribal knowledge"-krav
- [ ] Skript fungerar i Docker/CI på samma sätt som lokalt
- [ ] Sökvägar är relativa eller via miljövariabler

### Exempel: package.json (Node.js)

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

### Exempel: Makefile (Python)

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

### Exempel: scripts/ci.sh (Bash)

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

### Loggfiltrering för agenter

Agenter läser all output som feedback. Behandla loggar som ett gränssnitt till en automatiserad medarbetare:

**Bra: Koncis vid framgång**
```
✅ 1000 tests passed in 2.3s
```

**Dåligt: Brusig vid framgång**
```
test 1: ok
test 2: ok
test 3: ok
... (997 more lines)
```

**Bra: Åtgärdbart vid misslyckande**
```
FAIL: src/auth.test.ts:42
Expected: "user@example.com"
Received: "admin@example.com"
```

**Dåligt: Rörigt vid misslyckande**
```
[1000 lines of stack trace and compiler output]
```

### Determinism-exempel

**Problem: Icke-deterministiska tester**

```javascript
// Dåligt: använder nuvarande tid
expect(result).toBe(new Date().toISOString());

// Bra: deterministisk
expect(result).toBe("2026-01-14T12:00:00Z");
```

**Problem: Race conditions**

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

Detta är "kontextkonstruktion" i praktiken: designa I/O så att modellen ser signal, inte brus.

---

## 7) Lita på loopen, inte dina ögon

Agentbaserade arbetsflöden skalar när du kan låta agenten köra utan konstant övervakning.

För att komma dit behöver du:
- deterministiska byggen
- pålitliga tester
- linters/formatters
- tydliga exit-koder
- stabila skript

En stark harness gör det säkert att delegera:
- agenten ändrar kod
- kör validering
- läser misslyckandena
- itererar tills grönt
- presenterar en sammanfattning och den slutliga diffen

Din roll blir verifiering-via-kontrakt: "Möter den specen och passerar kontrollerna?"

---

## 8) Designa för svarta lådor

Agentbaserad utveckling belönar modularitet.

Föredra komponenter som är:
- små
- testbara i isolering
- definierade av tydliga inputs/outputs
- utbytbara utan att skriva om världen

Tänk "svarta lådmoduler", inte nödvändigtvis mikrotjänster:
- ett CLI-verktyg med stabila flaggor
- ett bibliotek med ett smalt gränssnitt
- en tjänst med en strikt API-gräns
- en pipeline-steg med explicita artefakter

Detta minskar mängden kod modellen måste hålla sammanhängande på en gång och gör refaktoreringar säkrare.

---

## 9) CLI före IDE (för agenter)

IDE-integrationer kan vara bekväma, men CLI har strukturella fördelar för agentbaserat arbete:

- **Upptäckbarhet:** `--help` lär ut verktyg utan extra kontext
- **Determinism:** skript beter sig samma i CI som lokalt
- **Transparens:** stdout/stderr är ett explicit gränssnitt du kan justera
- **Komponerbarhet:** lätt att kedja steg till ett kommando

Ett bra CLI-först arbetsflöde gör det också lättare att köra flera agentsessioner parallellt, eftersom varje session kan arbeta genom skript snarare än UI-tillstånd.

Om din miljö är icke-POSIX (eller skiljer sig från vad dina verktyg förväntar sig), överväg:
- WSL
- devcontainers
- standardiserade shell-skript
- konsekvent sökvägshantering

Målet är inte "ett OS är bäst", utan "ta bort friktion som skapar verktygsmisslyckanden och brusiga loggar".

---

## 10) TDD blir ovanligt effektivt med agenter

Klassisk, strikt Test-Driven Development kan kännas dyrt för människor. Med agenter skiftar ekonomin eftersom tester blir en ratt:

1. Skriv ett misslyckat test (eller en misslyckad kontroll)
2. Låt agenten implementera ändringen
3. Iterera tills grönt

Detta fungerar särskilt bra när:
- krav är skarpa
- kantfall är testbara
- framgång är observerbart via påståenden

### Skydd mot "fusk"
Agenter kan ibland tillfredsställa tester på ytliga sätt (mockar för mycket, hårdkodar, kringgår logik). Motåtgärder:
- lägg till egenskapsbaserade tester där lämpligt
- testa flera fall (inte bara "happy path")
- verifiera integrationsbeteende, inte bara enhetsbeteende
- inkludera negativa tester och invarianter

---

## 11) Golden master-testning för portar och refaktoreringar

När du migrerar system eller gör stora refaktoreringar kan golden master-testning vara extremt effektiv:

- instrumentera det gamla systemet för att emittera deterministiska spår (beslut, nyckelstatus, utdata)
- spara spåret som "golden"-filen
- implementera det nya systemet
- säkerställ att det matchar golden-spåret byte-för-byte (eller via en normaliserad komparator)

Detta är kraftfullt för:
- språkmigreringar
- parser/serializer-omskrivningar
- algoritmrefaktoreringar
- "samma beteende, annan implementation"-projekt

Om spår innehåller icke-deterministiska värden (tidsstämplar, pekare, slumpmässiga frön), normalisera dem.

---

## 12) Spendera tid på planering (och gör den återanvändbar)

Agenter gynnas av planer som är:
- stegade
- explicita om begränsningar
- explicita om "klart"
- nedskrivna inuti repot

En bra plan svarar på:
- vad bygger vi?
- vad är icke-målen?
- vad är gränssnitten?
- vad är invarianterna?
- vilka tester bevisar korrekthet?
- i vilken ordning ska ändringar landa?

Modeller är också användbara som planeringsassistenter:
- be om arkitekturalternativ
- begär risklistor
- generera ett fasat implementationsförslag
- identifiera saknade acceptanskriterier

Men planen måste i slutändan reflektera *dina* begränsningar och prioriteringar.

---

## 13) DevDocs: överlev kontextåterställningar

Långa sessioner tappar lätt fokus. En praktisk teknik är att hålla lättvikts "agent handoff"-dokument i repot, t.ex.:

```
devdocs/
  plan.md
  progress.md
  decisions.md   (valfritt)
  notes.md       (valfritt)
```

Föreslagna innehåll:

**devdocs/plan.md**
- mål / icke-mål
- arkitekturskiss
- faser
- acceptanskriterier
- kommandon att köra

**devdocs/progress.md**
- nuvarande tillstånd
- vad som är gjort (kryssrutor)
- vad som är nästa
- kända problem
- länkar till relevanta filer

När en session blir rörig eller kontexten fylls:
- starta en ny session
- peka agenten på `devdocs/plan.md` + `devdocs/progress.md`
- fortsätt med rent blad

Nyckelmentalitet: **planer och begränsningar är beständiga; kod är utbytbart.**

---

## 14) Ackumulering och "slop"-risk

En verklig oro i agentbaserad utveckling är långsiktig kodkvalitetsdrift:
- inkonsekventa mönster
- övervuxna abstraktioner
- duplicerad logik
- otydliga gränser

Mildringar:
- tvinga formatering och linting
- kräv tester för ändringar
- upprätthåll en arkitektur/beslutslogg
- refaktorera medvetet i faser
- periodiskt "åter-härled" moduler från en ren spec (när motiverat)
- håll moduler små och utbytbara

Behandla agenten som en höggenomsättlig bidragsgivare: utan styrning ackumuleras entropi.

---

## 15) Bortom kodning: var agenter lyser

Agentbaserade loopar är ofta mest värdefulla för arbete som är:
- nödvändigt men inte intellektuellt centralt
- mycket iterativt
- verktygsdrivet
- lätt att validera

Exempel:
- fixa CI-misslyckanden
- uppdatera byggskript
- repositoryhygien (lint, formatering, beroendeuppgraderingar)
- forskning om okända kodvägar
- generera minimala repros
- skriva migreringsskript
- operativ felsökning (när säkert och kontrollerat)

Det gemensamma temat: loopen har tydlig verktygsfeedback och begränsad risk.

---

## 16) Sub-agenter och delegeringsmönster

Ett skalningsmönster är att separera:
- **utforskning** (läsa kod, kartlägga flöden, identifiera filer)
från
- **exekvering** (applicera ändringar, köra kontroller, förfina)

Du kan modellera detta som:
- en "scout"-agent som returnerar en kort rapport:
  - var den relevanta logiken lever
  - hur call-grafen ser ut
  - vad som ska ändras och varför
- en "builder"-agent som implementerar och validerar
- ett "reviewer"-steg som sammanfattar diffar och risker

Detta hjälper kontrollera kontexttillväxt och minskar trashing.

---

## 17) En praktisk startchecklista

Om du vill att agentbaserad utveckling ska kännas produktiv snabbt, börja här:

**Repository harness**
- [ ] Ett kommando: bygg + test + lint  
- [ ] Tydliga skript i `./scripts` eller `Makefile`
- [ ] Minimala loggar vid framgång, åtgärdbara loggar vid misslyckande
- [ ] Deterministiska testkörningar

**Arbetsflöde**
- [ ] Skriv acceptanskriterier först
- [ ] Lägg till tester före eller tillsammans med ändringar
- [ ] Håll ändringar små och komponerbara
- [ ] Föredra moduler med smala gränssnitt

**Kontexthygien**
- [ ] Klistra inte in stora loggar/diffar om det inte är nödvändigt
- [ ] Tillhandahåll målinriktade filsökvägar och mål
- [ ] Använd `devdocs/` för beständig plan/framsteg

**Kvalitetskontroller**
- [ ] Linter + formatter + CI-grind
- [ ] Golden master-approach för riskfyllda migreringar
- [ ] Periodiska refaktoreringsfaser för att minska drift

---

## Avslutning

"Vibe Engineering" blir verkligt när du behandlar agenter som en del av ett system: en loop med verktyg, begränsningar och feedback. Om du investerar i harnessen och gör "klart" maskinkontrollerbart, kan du delegera säkrare, röra dig snabbare och spenderar mer tid på de konstruktionsbeslut som faktiskt spelar roll.
