# Agents.md förklarat: en praktisk guide till tillförlitlig agentisk AI
**Version 1.0** | 2026-01-22

## Ingress: vad Agents.md är, varför det finns och varför det är viktigt

När AI‑baserade kodverktyg utvecklades från enkel autocomplete till autonoma eller semi‑autonoma *agenter* uppstod snabbt ett nytt grundproblem: **kontext**.

Varje gång en agent börjar arbeta behöver den förstå:
- hur projektet byggs
- hur det testas
- hur koden är strukturerad
- vad den absolut inte får göra

Utan denna information gissar agenten. Ibland rätt, ofta fel. Resultatet blir upprepningar, inkonsekvens och subtila fel som kostar tid.

`agents.md` (och motsvarigheter som `CLAUDE.md` eller Cursor‑regler) uppstod som en enkel lösning:
**en liten, persistent instruktionsfil som automatiskt laddas när en agent arbetar i ett repo.**

Målet är inte att beskriva allt, utan att ge **precis tillräcklig gemensam kontext** så att:
- du slipper upprepa dig
- agenten beter sig konsekvent
- nya sessioner startar "varma"

I dag är vi i ett läge där:
- agenter klarar verkligt utvecklingsarbete
- kontextfel är den största begränsningen
- team som hanterar kontext väl rör sig betydligt snabbare

## Varför Agents.md är avgörande: från demo till tillförlitlighet

Agentisk AI är lätt att demonstrera – och svår att lita på.

Många team upplever samma sak:
- agenten ser imponerande ut i början
- den löser några uppgifter korrekt
- beteendet blir sedan inkonsekvent
- små ändringar ger oväntade fel
- människor kliver in och övervakar

Då har agenten slutat vara en multiplikator och blivit en risk.

Orsaken är sällan modellen.
Det är nästan alltid **saknad eller instabil kontext**.

### Tillförlitliga agenter kräver stabil kontext

För att fungera i verkligt utvecklingsarbete måste en agent vara:
- förutsägbar
- repeterbar
- konsekvent över tid

Människor lutar sig mot konventioner, verktygsstandarder och institutionsminne.
Agenter har inget av detta om du inte ger det till dem.

Utan `agents.md` startar varje session kall. Agenten gissar:
- hur man bygger
- hur man testar
- hur projektet är organiserat
- vad som är säkert att röra

Denna osäkerhet bryter förtroende.

### Agents.md gör antaganden till kontrakt

`agents.md` ersätter implicita antaganden med explicita kontrakt.

I stället för:
"Agenten borde veta detta…"

säger du:
"Så här fungerar det hos oss."

Det handlar inte om att göra agenten smartare.
**Det handlar om att göra den pålitlig.**

### Förtroende byggs genom att eliminera felklasser

De största vinsterna kommer inte från snabbare kod, utan från att
**aldrig behöva rätta samma AI‑misstag två gånger**.

Genom att koda in:
- faktiska kommandon
- hårda gränser
- stabila antaganden

elimineras hela klasser av fel permanent.

## Den centrala begränsningen: uppmärksamhet är ändlig

Alla LLM‑baserade agenter har en hård begränsning: **uppmärksamhetsbudget**.

För mycket kontext försämrar resonemang.
För lite leder till hallucinationer.

`agents.md` laddas tidigt och permanent i kontextfönstret.
Varje onödig rad tränger undan verkligt arbete.

## Hur Agents.md laddas: en mental modell

- Plats 0: system‑/harness‑prompt (verktygsstyrd)
- Plats 1: `agents.md` (användarstyrd, persistent)
- Plats 2+: arbetsminne (uppgifter, loggar, resonemang)

Allt på plats 1 måste vara minimalt, stabilt och högvärdigt.

## Compounding Engineering

Compounding Engineering innebär att:
**varje smärtsam interaktion med en agent förbättrar nästa.**

I stället för att upprepa korrigeringar kodar du in begränsningar och arbetssätt så att beteendet förbättras över tid.


## Modellkänslighet: varför samma Agents.md fungerar olika mellan modeller

Ett vanligt antagande är att en `agents.md`‑fil är neutral – att den fungerar likadant oavsett modell.

I praktiken stämmer inte detta.

Olika modeller tolkar *samma instruktioner* på olika sätt. Detta blir särskilt tydligt när man jämför OpenAI‑modeller med Anthropics Claude‑modeller, vilket Geoffrey Huntley visar i sitt föredrag.

I hans exempel gav samma `agents.md`:
- tydligt och beslutsamt beteende hos en OpenAI‑modell
- mer tveksamt och överdrivet försiktigt beteende hos en Claude‑modell

Filen var oförändrad. Det som ändrades var modellen.

Skillnaderna beror bland annat på hur modeller:
- tolkar begränsningar
- reagerar på ton och betoning
- tar initiativ
- balanserar försiktighet mot handling

Eftersom `agents.md` normalt laddas på plats 1 i kontextarrayen, direkt efter systemprompten, förstärks dessa skillnader. Små formuleringar kan ge stora beteendeskillnader.

Den centrala insikten är:

**Agents.md är inte bara konfiguration – det är beteendeprogrammering, och beteende är modellberoende.**

Vid byte av modell bör man därför:
- återvalidera agentens beteende
- observera tvekan eller övermod
- hellre regenerera än att lappa filen

Tillförlitlighet uppstår inte genom att välja "bästa" modellen, utan genom att justera **instruktioner, modellbeteende och förväntningar** så att de stämmer överens.

## Ett kompakt exempel på en bra agents.md

```md
## Commands
- Build: npm run build
- Test: npm test

## Structure
- src/: applikationskod
- test/: tester

## Stack
- Node.js 20
- TypeScript 5.x

## Boundaries
- Never commit secrets
- Never delete failing tests
```

## TL;DR

- Stabil kontext ger pålitliga agenter
- `agents.md` är hög hävstång och dyr kontext
- Håll den liten och explicit
- Eliminera upprepade fel
- Målet är förtroende, inte imponerande output

## Referenser & Credits

### Officiella resurser

- [agents.md](https://agents.md/)
- [Using CLAUDE.md Files — Anthropic](https://www.claude.com/blog/using-claude-md-files)
- [How to Write a Great agents.md — GitHub Blog](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)

### Inspiration

- [Grit AI Studio](https://www.youtube.com/@GritAIStudio)
- [Geoffrey Huntley](https://ghuntley.com/)

## agents.md / CLAUDE.md Template

Det här kapitlet innehåller en kopiera‑klistra‑mall för `agents.md` eller `CLAUDE.md`. Håll den repo‑specifik, kort och tydlig — målet är stabil, återanvändbar kontext som gör agenten pålitlig.

### Tom mall (kopiera och anpassa)

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

### Fyllda exempel

#### Node.js / TypeScript

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

#### Python

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

#### C# / .NET

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

### Best Practices

#### Håll den kort
- Fokusera på repo‑specifika regler, inte generella förklaringar
- Undvik att förklara vad "komponenter" är — modellen vet redan det

#### Förklara "varför"
- "Använd TypeScript strict mode eftersom implicit any orsakade produktionsbuggar"
- Detta hjälper modellen göra bättre bedömningar i kantfall

#### Uppdatera kontinuerligt
- Varje gång du korrigerar samma misstag två gånger, lägg till en regel
- Varje fix förhindrar framtida omarbete

#### Var specifik
- "Never commit secrets" är bra
- "Never commit secrets, check `.env.example` för format" är bättre

### Relaterade artiklar

- [Claude Code 101](claude-code-101.html) — specifikt för CLAUDE.md
- [Vibe Engineering 101](vibe-engineering-101.html) — hur du sätter upp validering och harness
