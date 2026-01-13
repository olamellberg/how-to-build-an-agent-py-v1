# Agentisk AI i IDE:n för .NET-backend och JavaScript-frontend (januari 2026)

Agentisk AI i en IDE handlar om mer än “autocomplete”. Det är arbetsflöden där assistenten kan **planera**, föreslå **diffar över flera filer**, köra **build/test/lint**, läsa felutskrifter och iterera mot tydliga acceptanskriterier. För den generella metodiken (harness, feedback-loop, kontexthygien) hänvisas till dina befintliga texter om agentloopar och “model CI”. fileciteturn2file6L10-L24 fileciteturn2file7L18-L27

Den här artikeln fokuserar därför på det som är **IDE-specifikt**: vilka IDE:er som är relevanta utan JetBrains, vilka modellfamiljer de typiskt ger tillgång till, hur agentflöden ser ut i praktiken för .NET + JS, samt vad det kostar (indikativt).

---

## 1) Vad du väljer när du “väljer IDE + agent”
I praktiken väljer du fyra saker samtidigt:

1) **Kontextmotor**: hur editor/agent samlar in relevanta filer och diffar.  
2) **Agentförmågor**: plan-läge, multi-file edits, körning av kommandon, PR-hjälp.  
3) **Modellportfölj**: vilka modellfamiljer (OpenAI/Anthropic/Google m.fl.) du kan välja för olika uppgifter. GitHub Copilot har t.ex. en officiell lista över vilka modeller som stöds i Copilot Chat. citeturn1search3  
4) **Styrning/kostnad**: licenser, usage/premium requests, team policies.

---

## 2) Kompakt matris: IDE ↔ modeller ↔ agentförmåga ↔ pris

> **Pris** = listpris i USD (exkl. moms), avrundat och indikativt. Funktioner och modellutbud kan variera per plan och kan ändras över tid.

| IDE / editor | AI-assistenter (exempel) | Modellfamiljer och bolag (exempel) | Agentiskt stöd (praktiskt) | Indikativt pris |
|---|---|---|---|---|
| **VS Code** | GitHub Copilot • Gemini Code Assist • Amazon Q Developer • (ev. BYOK via Continue) | Copilot: modellval i Copilot Chat från flera leverantörer (se “AI models for GitHub Copilot”). citeturn1search3 • Gemini Code Assist: Google (Gemini). citeturn0search9turn0search1 • Amazon Q Developer: AWS-tjänst för agentisk kodassistans. citeturn0search2 | Multi-file diffar, plan/agent-lägen (planberoende), och loop “ändra → kör checks → iterera”. | Copilot Pro **$10/mån**, Pro+ **$39/mån**. citeturn1search2turn1search14 • Amazon Q Developer Pro (listpris): **$19/anv/mån**. citeturn0search2 • Gemini Code Assist: Standard/Enterprise via Google Cloud-prissättning. citeturn0search1turn0search13 |
| **Visual Studio** | GitHub Copilot | Copilot-modeller enligt GitHub (se “AI models for GitHub Copilot”). citeturn1search3 | Agentisk chat/edit i IDE:n, bra match för .NET-slice (API + tester) när repo-harness finns. | Copilot-licenser enligt GitHub: Business **$19/anv/mån** (org) och individuella Pro/Pro+ enligt ovan. citeturn1search14turn0search0 |
| **Cursor** | Cursor (inbyggda agents + teamkontroller) | Modellkostnader och styrning dokumenteras i Cursor pricing (usage-baserat, per modell). citeturn1search1turn0search3 | AI-native agentik: multi-file, agent-run, och team-styrning kring spend limits. citeturn0search3turn1search1 | Teams: spend controls och modellpriser via Cursor. citeturn0search3turn1search1 |
| **Windsurf** | Windsurf (Cascade) | Modellutbud/premium-modeller styrs av Windsurf-plan och credits. citeturn1search0 | AI-native agentflöde via Cascade (multi-step i editorn). | Windsurf prissida (planer för individer/teams/enterprise). citeturn1search0 |

**Tolkning för .NET + JS-team:**  
- Vill du ha “standardiserbar enterprise-default” i Microsoft-ekosystemet: **VS Code/Visual Studio + Copilot** är det mest förutsägbara alternativet att rulla ut brett (licenser och dokumentation finns tydligt hos GitHub). citeturn1search14turn1search3  
- Vill du ha Google-spår i IDE:n: **Gemini Code Assist** är Googles förstahandsval för IDE-assistans. citeturn0search9turn0search13  
- Vill du ha “AI-first editor” med stark agentupplevelse: **Cursor/Windsurf** är ofta mer aggressiva i agentflöden, men blir också mer “plattform” att standardisera och kostnadsstyra. citeturn1search1turn1search0

---

## 3) Rekommenderade startpaket för team (praktiskt)
Här är tre “baseline”-paket som brukar fungera utan att skapa onödigt verktygskaos:

### Paket A: Microsoft-standard (mest kompatibelt)
- **VS Code för JS/TS och polyglot**
- **Visual Studio för .NET** (när det ger mervärde i debug/profiling)
- **GitHub Copilot som gemensam AI-bas**

Det här gör det enklare att skapa gemensamma riktlinjer för modellval, prompts, och arbetssätt i teamet (eftersom Copilot-koncepten är samma i båda IDE:erna). citeturn1search3turn1search14

### Paket B: Google-spår i IDE:n
- **VS Code**
- **Gemini Code Assist** (Standard/Enterprise om ni behöver org-funktioner)

Gemini Code Assist finns i “for individuals” samt Standard/Enterprise och dokumenteras via Google Developer/Cloud-dokumentation. citeturn0search9turn0search13turn0search1

### Paket C: AI-first editor
- **Cursor** eller **Windsurf** för team som vill driva agentik hårdare i editorn
- Tydlig spend-control/process för att undvika kostnadsöverraskningar (Cursor beskriver spending controls i Teams). citeturn0search3turn1search1

---

## 4) Praktiska agentiska arbetsflöden i IDE:n (komprimerat, med hänvisningar)
I stället för att upprepa grunderna från dina tidigare artiklar, bygger den här sektionen en **IDE-anpassad checklista** som kan kopieras till teamets working agreement.

### 4.1 Standardloop i IDE:n: “Plan → Diff → Check → Iterera”
- **En enda valideringssignal** (t.ex. `make check` eller `./scripts/ci.sh`) är den viktigaste acceleratorn för agentik. fileciteturn2file7L18-L27  
- Agentik skalar när du kan “lita på loopen” (agent gör ändringar, kör checks, itererar tills grönt, och presenterar diff + risker). fileciteturn2file9L14-L21  
- Om du vill ha en komplett metodbeskrivning (harness, kontext som “RAM”, loggdesign): se *Vibe Engineering 101*. fileciteturn2file6L28-L39 fileciteturn2file7L29-L43  

### 4.2 .NET: “Vertikal slice” som standarduppdrag
Kör agenten på uppdrag som har tydliga steg och tydlig verifiering:
- Endpoint + domänregel + persistence + tester (och ev. swagger/kontrakt)
- Små diffar (max 3–7 filer per iteration)
- `dotnet build` + `dotnet test` efter varje batch

Det här matchar “tool-driven, easy to validate”-kategorin där agentloopar typiskt ger bäst effekt. fileciteturn2file2L5-L20  

### 4.3 JS/TS: “Feature + states + test”
Låt agenten arbeta runt:
- UI-states (loading/error/success)
- tydlig felhantering (409/400/500)
- lint/test/build som grind

Och håll loggar minimala och målinriktade – överlastad kontext försämrar agentens precision. fileciteturn2file7L29-L41  

### 4.4 Reset-regel när sessionen degraderar
När agenten börjar “snurra” är det ofta snabbare att nollställa än att rädda en stökig kontext. Din befintliga rutin `/compact` → `/clear` → klistra in plan + constraints + aktuella fel är en bra standard. fileciteturn2file4L1-L11  

---

## 5) Skydda känslig kod/info (samlat, utan att ligga i tabellen)

Här är den korta, praktiska versionen som går att operationalisera. För principerna om varför stabil kontext och “contracts” (agents.md) är centrala för tillit, se *Agents.md Explained*. fileciteturn2file0L6-L36

### 5.1 Minimera dataytan som kan lämna maskinen
- Skapa en **AI-allowlist** för vilka mappar agenten får läsa (t.ex. `/src`, `/tests`) och en **denylist** för allt som aldrig får in i kontext (`/secrets`, cert, prod-config, kundexporter).
- Begränsa auto-indexering/”project scanning” i känsliga repos om verktyget stödjer det (målet är att agenten bara ser det som behövs för uppgiften).

### 5.2 Styr agentens verktyg och nätverksförmåga
- Kör agentens kommandon via en **kontrollerad harness** (script/Makefile) i stället för fri exekvering.
- Whitelista kommandon (build/test/lint) och kräv mänskligt godkännande för riskområden (auth, crypto, infra, licenser, secrets).

### 5.3 Stabilisera beteende med repo-kontrakt (agents.md)
Ett kort `agents.md` (eller motsvarande) som alltid innehåller:
- “Commands” (build/test/lint)
- “Structure” (viktiga mappar)
- “Boundaries” (vad agenten aldrig får göra)

Det minskar slumpen mellan sessioner och bygger tillit genom att eliminera återkommande felklasser. fileciteturn2file15L1-L11 fileciteturn2file0L59-L68  

### 5.4 Driftkrav: logga verktygsutfall och kör evals
För agentik i produktion (även internt) bör ni behandla modellen som en komponent i en pipeline: verktyg ger sanning, modellen skriver förslag, och ni mäter beteende med evals. *AI Fundamentals 2026* beskriver miniminivån tydligt (pipeline + evals). fileciteturn2file5L6-L21 fileciteturn2file11L9-L13  

---

## 6) Kostnads- och licensnoter (så ni kan budgetera rimligt)
- **Copilot**: individuella licenser (Pro/Pro+) och org-licenser (Business m.fl.) är tydligt specificerade av GitHub. citeturn1search14turn1search2  
- **Amazon Q Developer**: AWS listar prissättning och gränser för free/pro. citeturn0search2  
- **Gemini Code Assist**: prissättning och editions (Standard/Enterprise) dokumenteras i Google Cloud. citeturn0search1turn0search13turn0search9  
- **Cursor**: usage-baserat (modellpriser + token fee/spend controls i Teams). citeturn0search3turn1search1  
- **Windsurf**: prissida anger plan-uppdelning (free/teams/enterprise). citeturn1search0  

---

## 7) En kort “team-playbook” att införa vecka 1
1) Inför **en valideringscommand** (`make check` eller `./scripts/ci.sh`) och gör det till agentens standardverktyg. fileciteturn2file7L18-L27  
2) Lägg in `agents.md` med kommandon/struktur/boundaries (maximalt kompakt). fileciteturn2file0L59-L68  
3) Standardisera prompts: **Goal → Constraints/non-goals → Done → Plan först** (din “prompt som ingenjörskommunikation”-mall). fileciteturn2file4L21-L31  
4) Etablera en reset-regel: “om loopen degraderar → compact/clear och börja om rent”. fileciteturn2file4L1-L11  
5) För känsliga repos: aktivera denylist och begränsa agentverktyg enligt 5.1–5.2.
