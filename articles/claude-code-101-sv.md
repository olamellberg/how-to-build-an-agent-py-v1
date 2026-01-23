# Claude Code 101
**Version 1.0** | 2026-01-22

Officiell Claude Code-dokumentation: https://code.claude.com/docs/

## En praktisk handbok för att leverera riktiga ändringar säkert

Den här guiden är en **Claude Code-specifik** "101" för systemutvecklare. Målet är inte teori — det är en uppsättning repeterbara arbetsflöden som producerar **små diffar, snabb feedback och färre regressioner**.

---

## Tänk först (använd Plan Mode, exekvera sedan)

Claude Code fungerar bäst när första steget är att **strukturera problemet**, inte att skriva instruktioner.

### Varför detta spelar roll
Om förfrågan är bred kommer Claude fylla i luckor med "rimliga standardvärden". I ingenjörsarbete blir dessa ofta:
- onödiga abstraktioner
- för många filer
- dolda beteendeförändringar  
**Motivering:** tvetydighet ökar lösningsrymden, och modellen kommer utforska den.

### Vad du ska göra
1) **Skriv måltillståndet (acceptanskriterier) innan du ber om kod.**  
   **Motivering:** Claude är starkast när den optimerar för ett explicit "klart", inte ett underförstått.

2) **Använd Plan Mode för allt som påverkar arkitektur, data, auth eller gränssnitt.**  
   I Claude Code, gå in i Plan Mode (vanligtvis **Shift+Tab två gånger** beroende på setup).  
   **Motivering:** planering tvingar fram explicita gränser och minskar överraskande ändringar.

3) **Be om alternativ och avvägningar först, välj sedan.**  
   Exempelprompt:
   - "Lista 2–3 möjliga designs, peka ut risker, och rekommendera en. Skriv ingen kod ännu."  
   **Motivering:** den snabbaste vägen är ofta att välja rätt approach tidigt.

### Ersätt vagt med specifikt
Dåligt:
- "Bygg ett auth-system."

Bra:
- "Lägg till email/lösenord-auth med befintliga User-modellen; lagra sessioner i Redis med 24h utgång; skydda routes under `/api/protected`; inga nya beroenden; lägg till integrationstester."

**Motivering:** specificitet förhindrar övergrepp och skapar verifierbar output.

---

## Arkitektur är inte valfritt (det är hur du begränsar modellen)

Claude kan generera fungerande kod som bryter mot ditt systems invarianter. Lösningen är inte "bättre kodgenerering". Lösningen är **arkitekturbegränsningar i förväg**.

### Vad du ska inkludera i din planförfrågan
- **Gränser:** vilka moduler som kan/inte kan röra varandra
- **Invarianter:** vad som måste förbli sant
- **Icke-mål:** vad som inte får ändras
- **Validering:** kommandon som bevisar att det fungerar

**Motivering:** begränsningar fungerar som skyddsräcken; utan dem uppfinner Claude struktur.

---

## CLAUDE.md: din fil med högst hävstång

`CLAUDE.md` är en Markdown-fil som Claude Code läser vid sessionens start. Den fungerar som **beständiga repo-specifika instruktioner**.

### Varför det spelar roll
Det förvandlar upprepade korrigeringar till ett stabilt kontrakt:
- "använd detta testkommando"
- "formatera inte om orelaterade filer"
- "undvik nya abstraktioner"
- "följ dessa konventioner"

**Motivering:** beständig vägledning minskar promptlängd och ökar konsekvens mellan sessioner.

### Hur du skriver en bra CLAUDE.md
**Håll den kort.**  
Om du inkluderar för mycket kommer Claude ignorera instruktioner oförutsägbart.  
**Motivering:** instruktionsöverbelastning skapar prioritetskonflikter.

**Gör den repo-specifik.**  
Undvik generiska förklaringar ("vad komponenter är"). Inkludera de konstiga, lokala reglerna.  
**Motivering:** Claude känner redan till generella mönster; den behöver *dina* specifika.

**Förklara "varför", inte bara "vad".**  
- "Använd TypeScript strict mode eftersom implicit any orsakade produktionsbuggar."  
**Motivering:** "varför" hjälper Claude göra bättre bedömningar i kantfall.

**Uppdatera den kontinuerligt.**  
Varje gång du korrigerar samma misstag två gånger, lägg till en instruktion. Claude Code stödjer snabba sätt att fånga vägledning (ofta via en genväg som `#`, beroende på konfiguration).  
**Motivering:** detta ackumuleras — varje fix förhindrar framtida omarbete.

### En praktisk CLAUDE.md-starter (kopiera/klistra)
```md
# CLAUDE.md (project instructions)

## Goals
- Produce minimal, reviewable diffs.
- Prefer existing patterns in this repo.

## Non-goals
- Do not introduce new dependencies without explicit request.
- Do not reformat unrelated files.
- Do not create new abstractions unless asked.

## Commands (run after edits)
- Format: <cmd>
- Lint: <cmd>
- Typecheck: <cmd>
- Tests: <cmd>

## Architecture constraints
- Keep domain logic out of HTTP handlers.
- No DB access in middleware unless explicitly required.
- Keep public API backwards compatible by default.

## Working style
- Start with a 3–7 step plan.
- After each step: summarize diff + commands run + remaining risks.
- If uncertain: stop and ask for a decision.
```

---

## "Ultrathink"-läge (kvalitetsfokuserat mindset)

Vissa team använder en kort, högvärdig "kvalitetsribba" i sin projektvägledning för att få Claude att prioritera **genomtänkt planering, noggrann läsning och minimal komplexitet**. Detta kan ligga i `CLAUDE.md` (eller i en separat `QUALITY.md` som refereras från `CLAUDE.md`) så länge det förblir koncist.

### Principer att koda in (och varför de hjälper)

- **Tänk annorlunda:** ifrågasätt antaganden och överväg enklare arkitekturer före implementation.  
  **Motivering:** den första fungerande lösningen är ofta inte den bästa för långlivade system.

- **Var besatt av detaljer:** läs befintlig kod som en specifikation — följ etablerade mönster och namngivning.  
  **Motivering:** konsekvens minskar integrationsbuggar och håller diffar granskningsbara.

- **Planera som en designer:** skriv en kort plan som gör gränssnitt och invarianter explicita innan du redigerar filer.  
  **Motivering:** explicita gränser förhindrar trovärdig-men-felaktig kodgenerering.

- **Hantverk, inte spretighet:** håll funktioner och abstraktioner minimala; undvik att introducera nya lager om det inte efterfrågas.  
  **Motivering:** onödig inriktning ökar underhållskostnad och döljer defekter.

- **Iterera obevekligt:** validera efter varje steg (tester, skärmdumpar, jämförelser) och förfina tills det är korrekt och rent.  
  **Motivering:** frekvent feedback fångar regressioner tidigt och förkortar vägen till "klart".

- **Förenkla hänsynslöst:** ta bort komplexitet när den inte ger mätbart värde.  
  **Motivering:** enklare system misslyckas på färre sätt och är lättare att drifta.

### Verktygscues värda att fånga

- **Använd dina verktyg som instrument:** luta dig på bash-kommandon, MCP-servrar och anpassade slash-kommandon för repeterbara arbetsflöden.  
  **Motivering:** automation minskar manuella kopiera/klistra-fel och sparar tid.

- **Använd Git-historik som kontext:** kontrollera tidigare approaches och konventioner innan du uppfinner nya.  
  **Motivering:** historik avslöjar avsikt och minskar churn från "ny men inkonsekvent" implementationer.

- **Behandla mocks/skärmdumpar som specs när tillgängliga:** implementera mot det visuella/beteendemässiga målet.  
  **Motivering:** konkreta mål minskar tvetydighet och omarbete.

- **Använd flera Claude-sessioner medvetet:** separera planering vs exekvering, eller isolera orelaterade concerns.  
  **Motivering:** separation minskar kontextläckage och förbättrar fokus.

---

## Kontexthantering: avancerade tekniker

För grunderna (50%-regeln, när du ska starta nya sessioner), se [How to Master Claude Code](claude-code-mastery.html). Denna sektion täcker avancerade tekniker.

### En konversation per uppgift
Använd inte samma session för att bygga auth och refaktorera databaslager. Orelaterad kontext läcker och skapar felaktiga antaganden.

### Använd externa minnesfiler
Låt Claude skriva till `SCRATCHPAD.md`, `plan.md`, eller `devdocs/progress.md`. Filer består mellan sessioner och förankrar "sanningen" i repot.

### Kopiera-klistra reset-arbetsflöde
När saker blir uppsvällda:
- kör `/compact` för att få en sammanfattning
- kör `/clear` för att nollställa kontext
- klistra tillbaka endast den kritiska planen + begränsningar + aktuella fel

En liten, ren kontext överträffar ofta en stor, degraderad.

### Mental modell
Claude är i praktiken tillståndslös om du inte externaliserar tillståndet. Att förvänta sig minne som inte finns skapar inkonsekventa resultat.

---

## Prompting: behandla det som ingenjörskommunikation

Prompting är inte magi. Det är krav + begränsningar + verifiering.

### Använd en repeterbar promptstruktur
**Förfrågningsmall**
- Mål
- Kontext (filer/sökvägar)
- Begränsningar / icke-mål
- "Klart"-kriterier
- Be om plan först (sedan kod)

**Motivering:** strukturerad input minskar omarbete och gör output granskningsbar.

### Inkludera alltid "vad som inte ska göras"
Claude standardiserar ofta till extra abstraktion. Om minimalism spelar roll, säg det:
- "Håll detta enkelt. Inga nya filer om det inte är nödvändigt. Inga abstraktioner jag inte bad om."

**Motivering:** negativa begränsningar förhindrar scope-expansion.

### Inkludera "varför" när det påverkar avvägningar
Exempel:
- "Körs vid varje request → optimera för latens."
- "Prototyp att kasta → håll det minimalt."

**Motivering:** "varför" driver korrekta avvägningar.

---

## Arbetsflöde för modellval (håll det praktiskt)

Claude Code exponerar ofta olika modeller med olika avvägningar (hastighet vs djupare planering). Ett pålitligt mönster:

- Använd en starkare resonemangsmodell för **planering och avvägningar**
- Använd en snabbare modell för **implementation när planen är låst**

**Motivering:** planeringskvalitet är hävstång; exekveringshastighet spelar roll efter att beslut är tagna.

---

## MCP, hooks, slash-kommandon och config: använd features som tar bort slit

Claude Code har kraftfulla features. Poängen är inte "aktivera allt". Poängen är **ta bort upprepad friktion**.

### MCP (Model Context Protocol)
Använd MCP när du upprepat kopierar data från:
- GitHub
- Slack
- issue trackers
- databaser/API:er

**Motivering:** att automatisera kontextinhämtning minskar manuella fel och sparar tid.

### Hooks
Hooks kan köra kommandon före/efter ändringar:
- formatter på redigerade filer
- typkontroll efter redigeringar
- test-delmängd efter ett steg

**Motivering:** hooks förvandlar goda intentioner till automatisk upprätthållning.

### Anpassade slash-kommandon
Skapa återanvändbara promptar som kommandon via `.claude/commands/*.md`:
- `/review-pr`
- `/debug-failure`
- `/refactor-module`
- `/write-tests`

**Motivering:** att standardisera promptar ökar konsekvens i teamet.

### Inställningar/konfiguration
Använd config för att anpassa beteende:
- standardkommandon
- föredragen stil (små diffar, stanna-och-fråga vid osäkerhet)
- skyddsräcken (undvik nya deps, undvik breda refaktoreringar)

**Motivering:** konfiguration minskar prompt-overhead och drift.

---

## När Claude fastnar: bryt loopen medvetet

Fast-mönster:
- upprepar samma fix
- självsäker men fel ändringar
- oändligt "ett försök till"

### Vad du ska göra istället

**1) Nollställ kontext (`/clear`)**  
Ge sedan endast:
- uppgiftsbeskrivning
- begränsningar
- det specifika felet

**Motivering:** fast beteende korrelerar ofta med förorenad kontext.

**2) Gör uppgiften mindre**  
Be om en av:
- en minimal reproduktion
- en enfils-fix
- en test-first-ändring

**Motivering:** mindre sökrymder minskar fellägen.

**3) Visa ett konkret exempel**  
- "Här är det önskade outputformatet; applicera det på andra ställen."

**Motivering:** exempel är otvetydiga framgångsmått.

**4) Omformulera**  
- "Behandla detta som en tillståndsmaskin."
- "Skriv detta som rena funktioner med explicita inputs/outputs."

**Motivering:** vissa formuleringar mappar bättre mot modellens resonemang.

---

## Bygg system, inte engångsinteraktioner (headless mode)

Claude Code kan användas bortom interaktiva sessioner. I synnerhet:
- headless-körningar (t.ex. via en `-p` prompt-flagga i vissa uppsättningar)
- skriptade kedjade arbetsflöden
- automatiserad PR-granskning / dokumentuppdateringar

**Motivering:** automation förvandlar individuella vinster till repeterbar genomströmning.

### Ett säkert automationsmönster
- kör på ett smalt scope (enskild katalog / filmönster)
- logga output
- kräv CI-pass före merge
- behåll mänsklig granskning för riskfyllda domäner

**Motivering:** avgränsad automation är granskningsbar och minskar oavsiktliga ändringar.

### Förbättringssvänghjulet
- Claude gör ett misstag
- fånga regeln i `CLAUDE.md` eller en kommandomall
- lägg till en hook/check för att förhindra upprepning

**Motivering:** systematiska fixes ackumuleras.

---

## TL;DR (Claude Code 101)

- **Tänk först, skriv sedan:** Plan Mode producerar konsekvent bättre resultat.  
  **Motivering:** planering begränsar lösningsrymden.
- **Skriv arkitekturbegränsningar:** gränser + invarianter + icke-mål.  
  **Motivering:** förhindrar trovärdiga-men-felaktiga implementationer.
- **`CLAUDE.md` är hävstång:** håll den kort, repo-specifik och uppdaterad.  
  **Motivering:** beständiga instruktioner förbättrar varje session.
- **Kontext degraderas tidigt:** scope sessioner, externalisera minne, nollställ med `/compact` + `/clear`.  
  **Motivering:** mindre ren kontext slår stor brusig kontext.
- **Prompta som en ingenjör:** var explicit om klart-kriterier och vad som inte ska göras.  
  **Motivering:** minskar överengineering och omarbete.
- **Använd MCP/hooks/kommandon när de tar bort slit.**  
  **Motivering:** automation gör kvalitet repeterbar.
- **När fast, byt approach:** nollställ, förenkla, visa exempel, omformulera.  
  **Motivering:** loop-brytning slår brute force.
