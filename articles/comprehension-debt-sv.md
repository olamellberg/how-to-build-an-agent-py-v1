# Förståelseskuld: den verkliga flaskhalsen i agentisk mjukvaruleverans
**Version 1.0** | 2026-02-03
### Hur du konstruerar för granskningsbarhet när generering är billig

## Sammanfattning
Moderna kodagenter kan producera plausibla implementationer snabbt, ofta nå “ser klart ut” på minuter. Begränsningen har flyttats: ingenjörsteam är inte längre begränsade av att generera kod, utan av att verifiera korrekthet, bevara delad förståelse och integrera ändringar säkert i system med riktiga invarianter.

Den här artikeln definierar **förståelseskuld (comprehension debt)**: glappet mellan det du skeppat och det teamet kan förklara, felsöka och drifta. Den beskriver fellägena som driver den — **antagandespridning**, **abstraktionssvullnad**, **ackumulering av död kod** och **sykofantiskt instämmande** — och visar varför de ofta dyker upp *efter* första utkastet, när ändringar börjar interagera med produktionsverkligheten.

I stället för att “prompt:a bättre” föreslår artikeln en praktisk driftsmodell: behandla granskning som en pipeline med explicita budgetar (diffstorlek, scope), kräv evidensunderlag (körda kommandon + outputs + risknoter), tvinga fram borttagning och förenkling, och använd fresh-context reviews för att fånga konceptuella fel tidigt. Målet är att behålla agentisk hastighet **utan** att kodgranskning degenererar till gummistämpling.

## Vad den här artikeln fokuserar på
Den här artikeln fokuserar på:

- teamnivå‑begränsningar som håller PR:er granskningsbara
- verifieringsevidens och granskningschecklistor
- processmönster som minskar konceptuella fel

Den återberättar medvetet *inte*:

- harness‑setup och “one-command validation” (se *Vibe Engineering 101*)
- specmallar och kravstruktur (se *Spec-Driven Development*)
- grunderna i kontexthantering (se *Claude Code 101* / *How to Master Claude Code*)

## Artikelkarta
Om du har ont om tid, börja med avsnitt **4–7**. De innehåller de konkreta arbetssätten som gör att agentisk leverans kan skala *utan* gummistämpling.

1. **Den nya begränsningen**: från att skriva kod till att bevisa korrekthet
2. **Förståelseskuld**: definition, tidiga indikatorer och varför den växer
3. **Fyra fellägen**: konceptuella misstag agenter gör (och varför de består)
4. **Ingenjörskonst för granskningsbarhet**: diffbudgetar, scope och borttagning som standard
5. **Evidensunderlag**: artefakten som gör granskning skalbar
6. **Fresh-context review**: fånga konceptuella fel med rena indata
7. **Policyset för team**: copy/paste‑guardrails
8. **Vad ni ska mäta**: signaler på att verifiering blir er flaskhals

---

## 1) Den nya begränsningen: från “att skriva kod” till “att bevisa korrekthet”
Agentisk utveckling förändrar vad som är en bristvara.

När generering är billig slutar team vara begränsade av tangentryckningar. I stället blir flaskhalsen **verifiering**: att bevisa att en ändring är korrekt, säker att integrera och tillräckligt begriplig för att drifta senare. Addy Osmani kallar detta “80%-problemet”: agenter kan ofta ta dig till ett plausibelt första utkast snabbt, men sista biten domineras av integrationsverklighet och mänsklig granskningsbandbredd. ([addyo.substack.com](https://addyo.substack.com/p/the-80-problem-in-agentic-coding?utm_source=tldrdev))

### Den “sista 20%” är inte linjär
Den sista delen innehåller ofta arbete som är svårt att helt delegera eftersom det beror på systemets faktiska invarianter:

- **Kantfall**: sällsynta inputs, samtidighet, delvisa fel, tidszoner, behörigheter, datamigrationsquirks
- **Integrationskorrekthet**: kontrakt mellan moduler, bakåtkompatibilitet, utrullningsbegränsningar
- **Driftsäkerhet**: loggning, mätetal, larm, felsökningsvägar, rollback-planer
- **Prestanda & kostnad**: “det funkar”-utkastet som är för långsamt eller för dyrt
- **Säkerhet & regelefterlevnad**: antaganden om authz/authn, datahantering, attackyta

Om din process inte gör dessa kontroller billiga och upprepningsbara hamnar du i en paradox: **mer kod producerad, samma (eller sämre) leveransgenomströmning**.

### Den praktiska konsekvensen
I agentisk leverans är “granskningsbarhet” inte en trevlighet. Det är ett ingenjörskrav.

Ert system behöver kunna svara, för varje PR:

- Vad ändrades (beteendemässigt)?
- Vilken evidens säger att det fungerar?
- Vad kan gå sönder, och hur skulle vi märka det?
- Vad är rollback-historien om verkligheten inte håller med?

När ni inte kan svara snabbt har ni inte skeppat kod. Ni har skeppat **osäkerhet**.

---

## 2) Förståelseskuld: definition, tidiga indikatorer och varför den växer
**Förståelseskuld** är glappet mellan det ni skeppade och det teamet kan förklara, felsöka och drifta med hög tillit senare.

Den hänger ihop med (men skiljer sig från) teknisk skuld:

- **Teknisk skuld**: “vi förstår det, men det är fult/skört/långsamt och vi får betala senare.”
- **Förståelseskuld**: “vi skeppade det, men vi kan inte riktigt förklara det — vi satsar framtida tid på hopp.”

### Varför den växer
Förståelseskuld växer snabbare än linjärt eftersom varje oklar ändring gör det svårare att validera nästa.

När ni inte förstår en modul fullt ut tenderar ni att:

- skriva svagare tester (ni vet inte vad som ska assertas)
- missa invarianter (“det här måste alltid vara sant”)
- acceptera sköra abstraktioner (“det verkar rimligt”)
- granska på vibes i stället för evidens (“LGTM” blir en coping‑mekanism)

Med tiden blir granskning gummistämpling: er förmåga att **skilja** bra kod från plausibel kod hänger inte med agentens förmåga att **generera** plausibel kod. Osmani lyfter detta som en dold kostnad i produktivitetsnarrativet. ([addyo.substack.com](https://addyo.substack.com/p/the-80-problem-in-agentic-coding?utm_source=tldrdev))

### Tidiga indikatorer (varningssignaler)
Om flera av de här stämmer ackumuleras förståelseskuld redan:

- PR:er mergas med kommentarer som “ser bra ut” utan konkret verifieringsevidens
- PR-sammanfattningar beskriver *vilka filer* som ändrats men inte *vilket beteende* som ändrats
- reviewers frågar “varför behövs det här?” *efter* att koden är skriven (intent var inte förankrat)
- diffar innehåller ofta “drive-by”-refactors, renames och nya abstraktioner
- “tillfällig” kod blir kvar för alltid (feature flags, kommenterade block, alternativa paths)
- on‑call kan inte svara på “vad ändrades nyligen?” inom några minuter

Fixen är sällan “var mer försiktig.” Den är nästan alltid “konstruera arbetsflödet så att det är svårt att skeppa okända saker.”

---

## 3) Fyra fellägen att designa mot
Som Osmani noterar har många agentmisstag flyttat från uppenbara syntaxfel till **konceptuella fel**: sådant som ser koherent ut i en diff men bryter riktiga constraints senare. ([addyo.substack.com](https://addyo.substack.com/p/the-80-problem-in-agentic-coding?utm_source=tldrdev))

### 3.1 Antagandespridning
**Vad det är:** agenten gör ett tidigt antagande (“det här API:et beter sig som X”, “fältet finns alltid”) och bygger en koherent lösning ovanpå det.

**Hur det visar sig:**

- en refaktor ändrar betydelse subtilt (t.ex. tidszoner, nullability, casing, auth checks)
- ny logik speglar ett mönster som är *nästan* rätt men bryter en lokal invariant
- tester passerar eftersom de inte täcker den verkliga produktionsformen

**Motåtgärder:**

- Kräv en explicit **Antaganden**‑lista i PR:ens evidensunderlag.
- Lägg till en “prove it”‑check: tester för kantfall, kontraktstester eller en snabb integrationskörning.
- Gör ett kort “utforska först”‑steg: hitta befintligt mönster i kodbasen innan ni implementerar.

### 3.2 Abstraktionssvullnad
**Vad det är:** agenten introducerar onödiga lager (factories, managers, generiska frameworks) som ökar ytan och minskar tydligheten.

**Hur det visar sig:**

- en 20‑raders beteendeförändring blir 5 filer och en ny “arkitektur”
- abstraktioner som inte återanvänds (än) men tvingar alla att lära dem nu
- “flexibilitet” som aldrig behövs, i utbyte mot omedelbar komplexitet

**Motåtgärder:**

- Standardregel: **ingen ny abstraktion utan ett konkret återanvändningsfall**.
- Föredra enklaste korrekta implementation, extrahera först när upprepning uppstår.
- Upprätthåll **diffbudgetar** så svullnad inte kan gömma sig i en “stor men plausibel” PR.

### 3.3 Ackumulering av död kod
**Vad det är:** gamla implementationer ligger kvar, alternativa vägar förblir nåbara och “tillfällig” scaffolding blir permanent.

**Hur det visar sig:**

- duplicerade funktioner (“v1” och “v2”) finns båda “för säkerhets skull”
- feature flags utan borttagningsplan
- stora diffar som lägger till nytt beteende men inte tar bort det gamla beteendet

**Motåtgärder:**

- Bias mot **borttagning**: om ni lägger till en ny path, ta bort den gamla i samma PR (eller i en explicit schemalagd uppföljning).
- Behandla kommenterad kod som en lukt: ta bort den, lita på git-historiken.
- Lägg till statiska checks där det går (outnyttjade exports, unreachable code, coverage‑drop).

### 3.4 Sykofantiskt instämmande
**Vad det är:** agenten instämmer självsäkert och kör, även när krav krockar, är underspecificerade eller innebär tradeoffs.

**Hur det visar sig:**

- “sure!”‑implementationer som ignorerar non‑goals eller dolda prioriteringar
- ändringar som “funkar” men skiftar produktbeteende oavsiktligt
- saknad tradeoff‑diskussion (hastighet vs korrekthet, caching vs staleness, etc.)

**Motåtgärder:**

- Gör tradeoffs explicita i spec eller PR: “vi optimerar för X över Y.”
- Kräv en “Risker & tradeoffs”‑sektion i evidensunderlaget.
- Använd **fresh-context review** (avsnitt 6) för att tvinga kritik, inte fortsättning.

---

## 4) Ingenjörskonst för granskningsbarhet: diffbudgetar, scope och borttagning som standard
Om granskning är er flaskhals kan ni inte “fixa det” med mer prompting. Ni fixar det genom att designa arbetet så att det är granskningsbart som default.

### Diffbudgetar (gör PR:er läsbara i en sittning)
Välj budgetar som passar ert team, men gör dem explicita. Exempel på startpunkter:

- **En beteendeförändring per PR** (allt annat blir en uppföljnings‑PR)
- **Begränsa blast radius**: 1 subsystem, 1 publik interface eller 1 user-facing flow
- **Begränsa storlek**: t.ex. 200–400 LOC netto, ≤10 filer (justera efter er verklighet)
- **Begränsa nyhet**: ingen helt ny “framework”-nivå + beteendeförändring i samma PR

Rätt budget är den era reviewers klarar utan kontextkollaps. Om granskning ofta tar dagar är PR:erna för stora.

### Separera refaktor från beteendeförändring
Agenter är bra på att “städa upp”, men städning är dyr att verifiera när den blandas med beteendeförändring.

Två pragmatiska regler:

- Om det ändrar beteende måste det ha fokuserad verifiering (tester/evidens).
- Om det är “bara refaktor” ska det vara mekaniskt verifierbart (inga logikändringar) och landa separat.

### Borttagning som standard (bekämpa entropi)
När generering är billig växer system om ni inte aktivt tar bort.

I granskning, fråga:

- Vad tog vi bort?
- Vad blev enklare?
- Vilken gammal path behöver inte längre finnas?

Om en PR bara lägger till, månad efter månad, är förståelseskuld nästan garanterad.

---

## 5) Evidensunderlag: gör verifiering billig och återanvändbar
Ett **evidensunderlag** är en liten, standardiserad artefakt som följer med PR:en. Det svarar på “varför ska jag tro på detta?” utan att granskaren behöver återskapa hela agentsessionen.

Gör du det rätt blir det det första en reviewer läser och det sista du behöver när du felsöker en regression.

### Minimal mall för evidensunderlag (copy/paste)
Använd i PR-beskrivningar eller som obligatorisk checklista.

```md
## Evidensunderlag
- Mål:
- Icke-mål:
- Beteendeförändring (1–3 bullets):
  - ...
- Hur verifierat:
  - `command` (result)
  - `command` (result)
- Risker / kantfall:
  - ...
- Utrullning / rollback:
  - ...
- Antaganden:
  - ...
```

### Varför det fungerar
Evidensunderlag minskar förståelseskuld eftersom de:

- tvingar fram explicit intent (mål/icke‑mål)
- gör “lita på mig” till “här är vad jag körde”
- synliggör antaganden tidigt (innan de blir arkitektur)
- gör granskning mindre beroende av vem som genererade koden

---

## 6) Fresh-context review‑mönster
Långa agentsessioner skapar ett nytt problem: granskare kan inte (och ska inte) läsa hela historiken. Lösningen är att granska i en **fresh context**: behandla diff + evidens som input, inte konversationen.

### Människa: evidens-först-checklista
Innan du fastnar i implementationdetaljer, kolla fundamenten:

- Gör denna PR **en** sak?
- Är beteendeförändringen tydlig (inte bara “refaktor av X”)?
- Finns verifieringsevidens (tester/kommandon/output)?
- Är antaganden och risker utpekade?
- Lade vi till komplexitet som vi inte behöver direkt?
- Kan en kollega förklara ändringen i morgon utan agentchatten?

### Agent: “review från scratch”-prompt
Be en agent granska som om den saknade all tidigare kontext. Ge bara evidensunderlaget + diffen.

```text
Du granskar en PR. Använd enbart evidensunderlaget och diffen nedan.

Returnera:
1) Sammanfattning av beteendeförändringen (max 5 bullets)
2) Antaganden som måste stämma
3) Risker / kantfall / saknade tester
4) Onödig komplexitet (vad kan tas bort eller förenklas)
5) Go/No-Go och vad som skulle ändra det
```

Det här mönstret är särskilt bra för att fånga konceptuella fel (avsnitt 3) eftersom det tvingar kritik i stället för fortsättning.

---

## 7) Ett lättviktigt policyset för team (copy/paste)
Om ni vill ha agentisk hastighet utan att granskning kollapsar, anta ett minimalt policyset och följ det konsekvent.

```md
## Policy för granskningsbara PR:er (agentiskt arbete)
- En beteendeförändring per PR.
- Diffbudget: håll PR:er granskningsbara i en sittning (sätt teamnivå‑tal för LOC/filer/subsystem).
- Evidensunderlag krävs för alla beteendeförändringar.
- Refaktor och beteendeförändring landar separat.
- Inget nytt abstraktionslager utan ett konkret återanvändningsfall.
- Ta bort död kod (inga “tillfälliga” grenar utan borttagningsplan).
- Fresh-context review krävs när:
  - ändringen är högrisk (auth, pengar, behörigheter, datamigreringar)
  - diffen överskrider budget
  - reviewern inte kan förklara ändringen efter att ha läst PR:en en gång
```

Du kan klistra in detta i repo-handbok, PR-template eller till och med i er `agents.md` som en delad constraint.

---

## 8) Vad ni ska mäta: signaler på att verifiering blir er flaskhals
Om ni bara mäter “PR:er mergade” kommer agentiskt arbete se fantastiskt ut ända tills det kollapsar.

Mät verifieringssystemet.

### Signaler för granskningslast

- medianstorlek på PR (filer, LOC, “net change”)
- median tid till första review och tid till merge
- antal review‑rundor (kommentarcykler) per PR
- andel PR:er utan evidensunderlag (ska trenda mot ~0)

### Signaler för kvalitet & drift

- revert‑frekvens inom 24–72 timmar efter merge
- incidenter kopplade till “nyligen ändrat som vi inte riktigt förstod”
- tid att diagnosticera regressioner (om den ökar, ökar förståelseskulden)

### Förståelsesignaler (svårare, men värdefulla)

- slumpmässiga “förklara denna PR”‑spotchecks i review (klarar författaren 2 minuter?)
- onboarding‑tid till att bli effektiv i kodbasen
- “rädsla att röra”-områden (moduler alla undviker)

Om dessa trendar fel är fixen nästan alltid samma: mindre diffar, starkare evidens, färre antaganden och mer borttagning.

## Referenser
- Addy Osmani — “The 80% Problem in Agentic Coding” ([addyo.substack.com](https://addyo.substack.com/p/the-80-problem-in-agentic-coding?utm_source=tldrdev))
