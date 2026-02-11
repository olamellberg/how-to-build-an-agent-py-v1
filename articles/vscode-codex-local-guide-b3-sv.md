# VSCode + Codex Local: Från noll till agentisk utveckling
**Version 1.0** | 2026-02

En praktisk, hands-on guide för utvecklare som vill komma igang med OpenAI Codex i VSCode.

## Varfor Codex Local nu

Codex Local gor det mojligt att kora agentisk utveckling direkt i din editor och i ditt eget repo. Du far lokal exekvering, sandboxade kommandon och snabb iteration utan att lamna arbetsflodet.

## Installation och setup

1. Installera Codex-extensionen i VSCode.
2. Logga in med ditt ChatGPT-konto.
3. Oppna ett projekt i en lokal workspace.
4. Testa med en enkel prompt, till exempel: "Beskriv projektstrukturen i denna mapp."

## AGENTS.md och styrning

Skapa en `AGENTS.md` i repo-roten for att ge agenten tydliga regler:
- vilka kommandon som ska koras
- kodstandarder och arkitekturgranser
- vad som inte far andras

Detta minskar risk for onodiga diffar och gor resultatet mer konsekvent.

## Praktiskt arbetsflode

Ett bra startflode:
1. Beskriv malet tydligt med acceptanskriterier.
2. Referera relevanta filer med `@filnamn`.
3. Lat agenten foresla plan innan full implementation.
4. Granska diff, kor tester och iterera i sma steg.

## Vanliga fallgropar

- For breda promper ger ofta for stora och otydliga andringar.
- Saknad `AGENTS.md` leder till mer antaganden fran agenten.
- Avsaknad av tester gor det svart att veta om resultatet faktiskt fungerar.

## Sammanfattning

VSCode + Codex Local passar team som vill oka hastighet utan att tappa kontroll. Nyckeln ar tydliga instruktioner, sma verifierbara steg och ett stabilt arbetssatt med tester och code review.
