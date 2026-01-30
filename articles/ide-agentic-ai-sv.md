# Agentisk AI i IDE:n för .NET-backend och JavaScript-frontend
**Version 1.0** | 2026-01-22

Agentisk AI i en IDE handlar om mer än "autocomplete". Det är arbetsflöden där assistenten kan **planera**, föreslå **diffar över flera filer**, köra **build/test/lint**, läsa felutskrifter och iterera mot tydliga acceptanskriterier. För den generella metodiken (harness, feedback-loop, kontexthygien) hänvisas till dina befintliga texter om agentloopar och "model CI".

Den här artikeln fokuserar därför på det som är **IDE-specifikt**: vilka IDE:er som är relevanta utan JetBrains, vilka modellfamiljer de typiskt ger tillgång till, hur agentflöden ser ut i praktiken för .NET + JS, samt vad det kostar (indikativt).

---

## 1) Vad du väljer när du "väljer IDE + agent"
I praktiken väljer du fyra saker samtidigt:

1) **Kontextmotor**: hur editor/agent samlar in relevanta filer och diffar.  
2) **Agentförmågor**: plan-läge, multi-file edits, körning av kommandon, PR-hjälp.  
3) **Modellportfölj**: vilka modellfamiljer (OpenAI/Anthropic/Google m.fl.) du kan välja för olika uppgifter. GitHub Copilot har t.ex. en officiell lista över vilka modeller som stöds i Copilot Chat.  
4) **Styrning/kostnad**: licenser, usage/premium requests, team policies.

---

## 2) Kompakt matris: IDE ↔ modeller ↔ agentförmåga ↔ pris

> **Pris** = listpris i USD (exkl. moms), avrundat och indikativt. Funktioner och modellutbud kan variera per plan och kan ändras över tid.

| IDE / editor | AI-assistenter (exempel) | Modellfamiljer och bolag (exempel) | Agentiskt stöd (praktiskt) | Indikativt pris |
|---|---|---|---|---|
| **VS Code** | GitHub Copilot • Gemini Code Assist • Amazon Q Developer • (ev. BYOK via Continue) | Copilot: modellval i Copilot Chat från flera leverantörer. • Gemini Code Assist: Google (Gemini). • Amazon Q Developer: AWS-tjänst för agentisk kodassistans. | Multi-file diffar, plan/agent-lägen (planberoende), och loop "ändra → kör checks → iterera". | Copilot Pro **$10/mån**, Pro+ **$39/mån**. • Amazon Q Developer Pro (listpris): **$19/anv/mån**. • Gemini Code Assist: Standard/Enterprise via Google Cloud-prissättning. |
| **Visual Studio** | GitHub Copilot | Copilot-modeller enligt GitHub. | Agentisk chat/edit i IDE:n, bra match för .NET-slice (API + tester) när repo-harness finns. | Copilot-licenser enligt GitHub: Business **$19/anv/mån** (org) och individuella Pro/Pro+ enligt ovan. |
| **Cursor** | Cursor (inbyggda agents + teamkontroller) | Modellkostnader och styrning dokumenteras i Cursor pricing (usage-baserat, per modell). | AI-native agentik: multi-file, agent-run, och team-styrning kring spend limits. | Teams: spend controls och modellpriser via Cursor. |
| **Windsurf** | Windsurf (Cascade) | Modellutbud/premium-modeller styrs av Windsurf-plan och credits. | AI-native agentflöde via Cascade (multi-step i editorn). | Windsurf prissida (planer för individer/teams/enterprise). |
| **Claude Code** (Terminal) | Claude Code CLI | Anthropic (Claude Opus 4.5, Sonnet 4, Haiku). Direkt API-access utan mellanhand. | Fullt agentisk CLI: multi-file edits, bash-exekvering, git-operationer, plan-läge, sub-agenter. Fungerar i valfri terminal bredvid din IDE. | Anthropic API-prissättning (usage-baserat). Pro-plan inkluderar Claude Code-användning. |

**Tolkning för .NET + JS-team:**
- Vill du ha "standardiserbar enterprise-default" i Microsoft-ekosystemet: **VS Code/Visual Studio + Copilot** är det mest förutsägbara alternativet att rulla ut brett (licenser och dokumentation finns tydligt hos GitHub).
- Vill du ha Google-spår i IDE:n: **Gemini Code Assist** är Googles förstahandsval för IDE-assistans.
- Vill du ha "AI-first editor" med stark agentupplevelse: **Cursor/Windsurf** är ofta mer aggressiva i agentflöden, men blir också mer "plattform" att standardisera och kostnadsstyra.
- Vill du ha maximal agentisk kraft utan att byta IDE: **Claude Code** körs i din terminal bredvid valfri editor. Det erbjuder den mest kapabla agentloopen (plan-läge, sub-agenter, full bash-access) med direkt Anthropic API-åtkomst.

---

## 3) Rekommenderade startpaket för team (praktiskt)
Här är tre "baseline"-paket som brukar fungera utan att skapa onödigt verktygskaos:

### Paket A: Microsoft-standard (mest kompatibelt)
- **VS Code för JS/TS och polyglot**
- **Visual Studio för .NET** (när det ger mervärde i debug/profiling)
- **GitHub Copilot som gemensam AI-bas**

Det här gör det enklare att skapa gemensamma riktlinjer för modellval, prompts, och arbetssätt i teamet (eftersom Copilot-koncepten är samma i båda IDE:erna).

### Paket B: Google-spår i IDE:n
- **VS Code**
- **Gemini Code Assist** (Standard/Enterprise om ni behöver org-funktioner)

Gemini Code Assist finns i "for individuals" samt Standard/Enterprise och dokumenteras via Google Developer/Cloud-dokumentation.

### Paket C: AI-first editor
- **Cursor** eller **Windsurf** för team som vill driva agentik hårdare i editorn
- Tydlig spend-control/process för att undvika kostnadsöverraskningar (Cursor beskriver spending controls i Teams).

### Paket D: Terminal-first agentik (Claude Code)
- **Valfri IDE du redan använder** (VS Code, Visual Studio, Vim, etc.)
- **Claude Code** i en terminalruta eller separat fönster
- Bäst för utvecklare som vill ha starkast möjliga agentik utan att byta editor
- Claude Code läser `CLAUDE.md` (liknande `agents.md`) för repo-kontext, kör bash-kommandon, skapar PR:er, och kan starta sub-agenter för parallellt arbete
- Kombineras väl med lättviktsextensions (Copilot för autocomplete, Claude Code för tunga agentiska uppgifter)

---

## 4) Agentiska arbetsflöden i IDE:n
I stället för att upprepa grunderna från dina tidigare artiklar, bygger den här sektionen en **IDE-anpassad checklista** som kan kopieras till teamets working agreement.

### 4.1 Standardloop i IDE:n: "Plan → Diff → Check → Iterera"
- **En enda valideringssignal** (t.ex. `make check` eller `./scripts/ci.sh`) är den viktigaste acceleratorn för agentik.  
- Agentik skalar när du kan "lita på loopen" (agent gör ändringar, kör checks, itererar tills grönt, och presenterar diff + risker).  
- Om du vill ha en komplett metodbeskrivning (harness, kontext som "RAM", loggdesign): se *Vibe Engineering 101*.  

### 4.2 .NET: "Vertikal slice" som standarduppdrag
Kör agenten på uppdrag som har tydliga steg och tydlig verifiering:
- Endpoint + domänregel + persistence + tester (och ev. swagger/kontrakt)
- Små diffar (max 3–7 filer per iteration)
- `dotnet build` + `dotnet test` efter varje batch

Det här matchar "tool-driven, easy to validate"-kategorin där agentloopar typiskt ger bäst effekt.  

### 4.3 JS/TS: "Feature + states + test"
Låt agenten arbeta runt:
- UI-states (loading/error/success)
- tydlig felhantering (409/400/500)
- lint/test/build som grind

Och håll loggar minimala och målinriktade – överlastad kontext försämrar agentens precision.  

### 4.4 Reset-regel när sessionen degraderar
När agenten börjar "snurra" är det ofta snabbare att nollställa än att rädda en stökig kontext. Din befintliga rutin `/compact` → `/clear` → klistra in plan + constraints + aktuella fel är en bra standard.  

---

## 5) Skydda känslig kod/info (samlat, utan att ligga i tabellen)

Här är den korta, praktiska versionen som går att operationalisera. För principerna om varför stabil kontext och "contracts" (agents.md) är centrala för tillit, se *Agents.md Explained*.

### 5.1 Minimera dataytan som kan lämna maskinen
- Skapa en **AI-allowlist** för vilka mappar agenten får läsa (t.ex. `/src`, `/tests`) och en **denylist** för allt som aldrig får in i kontext (`/secrets`, cert, prod-config, kundexporter).
- Begränsa auto-indexering/"project scanning" i känsliga repos om verktyget stödjer det (målet är att agenten bara ser det som behövs för uppgiften).

### 5.2 Styr agentens verktyg och nätverksförmåga
- Kör agentens kommandon via en **kontrollerad harness** (script/Makefile) i stället för fri exekvering.
- Whitelista kommandon (build/test/lint) och kräv mänskligt godkännande för riskområden (auth, crypto, infra, licenser, secrets).

### 5.3 Stabilisera beteende med repo-kontrakt (agents.md)
Ett kort `agents.md` (eller motsvarande) som alltid innehåller:
- "Commands" (build/test/lint)
- "Structure" (viktiga mappar)
- "Boundaries" (vad agenten aldrig får göra)

Det minskar slumpen mellan sessioner och bygger tillit genom att eliminera återkommande felklasser.  

### 5.4 Driftkrav: logga verktygsutfall och kör evals
För agentik i produktion (även internt) bör ni behandla modellen som en komponent i en pipeline: verktyg ger sanning, modellen skriver förslag, och ni mäter beteende med evals. *AI Fundamentals 2026* beskriver miniminivån tydligt (pipeline + evals).  

---

## 6) Kostnads- och licensnoter (så ni kan budgetera rimligt)
- **Copilot**: individuella licenser (Pro/Pro+) och org-licenser (Business m.fl.) är tydligt specificerade av GitHub.  
- **Amazon Q Developer**: AWS listar prissättning och gränser för free/pro.  
- **Gemini Code Assist**: prissättning och editions (Standard/Enterprise) dokumenteras i Google Cloud.  
- **Cursor**: usage-baserat (modellpriser + token fee/spend controls i Teams).  
- **Windsurf**: prissida anger plan-uppdelning (free/teams/enterprise).  

