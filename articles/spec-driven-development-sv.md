# Spec-Driven Development: Praktisk guide
**Version 1.1** | 2026-01-29
### En praktisk guide till att bygga utifrån tydliga specs

## 1) Introduktion: problemet SDD löser

Specarbete faller ofta på två saker: antingen är det för vagt för att styra implementationen, eller för tungt för att användas konsekvent. I AI-assisterad utveckling blir detta ännu tydligare när kontexten växer, antaganden glider och små fel staplas.

SDD finns för att hålla intent stabilt medan execution itererar. Det skapar ett gemensamt mål, tajtar feedback-loopen och gör “klart” testbart.

---

## 2) Vad SDD är (och inte är)

**Spec-Driven Development (SDD)** innebär att du definierar avsett beteende innan du implementerar. Specen blir ankaret för beslut, scope och validering.

Det är ett lättviktigt sätt att ta bort oklarheter och göra “klart” verifierbart.

---

## 3) Varför SDD är viktigt just nu (kontext-rot)

När AI-sessioner blir långa sjunker kvaliteten ofta. Kontexten blir brusig, antaganden glider, och små misstag staplas. En spec är motgiftet: den håller målet stabilt medan modellen itererar.

SDD gör agentiskt arbete säkrare eftersom:
- kraven är explicita
- constraints är synliga
- validering är definierad i förväg
- loopen kan självkorrigera utan gissningar

---

## 4) SDD-livscykeln (utforska → planera → utföra → verifiera)

SDD är en loop, inte ett dokument.

1) **Utforska:** klargör det verkliga problemet, constraints och non-goals  
2) **Planera:** gör intent till testbara krav och gränssnitt  
3) **Utföra:** implementera i små, granskbara steg  
4) **Verifiera:** kontrollera mot tester/evals och skärp specen

Att hålla livscykeln explicit motverkar drift och håller kontexten fräsch.

---

## 5) Minsta fungerande spec (MVS)

En användbar spec kan vara kort. Minsta som fungerar:

- **Mål:** vilket utfall siktar vi på?
- **Klart-kriterier:** vad bevisar att det är klart?
- **Constraints:** gränser, non-goals, invariants
- **Input/output:** format, schema, gränssnitt
- **Exempel:** ett bra, ett dåligt
- **Validering:** tester eller checks att köra

När dessa sex punkter är tydliga blir implementationen rak.

---

## 6) Spec-struktur som skalar

När systemen växer behöver specs en konsekvent form:

1) **Kontext:** nuläge och constraints  
2) **Problem:** vad behöver ändras  
3) **Krav:** måste/bör/ska inte  
4) **Gränssnitt:** API:er, input/output, format  
5) **Validering:** tester, checks eller evals  

Detta håller specen kort men komplett och gör granskning enklare.

---

## 7) Gör krav testbara

Skriv krav som går att verifiera:
- “Måste returnera JSON med fälten X, Y, Z”
- “Måste klara `npm test`”
- “Får inte ändra public API”

Använd **Måste / Bör / Ska inte** för att undvika scope creep och göra prioriteringar tydliga.

---

## 8) Specar som körbara kontroller

I agentiskt arbete är **tester och evals körbara specs**. Om ett krav inte kan testas är det lätt att ignorera. Om det är kodat i checks så tvingar loopen fram det.

Tumregel: varje viktig constraint ska ha en konkret check.

---

## 9) Håll kontexten frisk med små steg

Kvaliteten sjunker när uppgifter blir för stora. Dela upp arbetet i små, atomiska steg med tydlig verifiering. Det minskar kontextbloat och gör feedback-loopen pålitlig.

Tecken på att det är för stort:
- flera orelaterade filer ändras samtidigt
- långa, tvetydiga prompts
- valideringssteg är oklara eller saknas

---

## 10) Greenfield vs brownfield-specar

**Greenfield:** fokusera på vision, gränser och non-goals för att undvika överbyggande.  
**Brownfield:** fokusera på kompatibilitet, invariants och regressionskontroller.

Samma specstruktur fungerar, men tyngdpunkten flyttar sig.

---

## 11) Minimal spec-mall

```md
# Spec: <feature name>

## Goal
<What outcome are we aiming for?>

## Success criteria
- ...
- ...

## Constraints / Non-goals
- ...

## Inputs / Outputs
- Input:
- Output:
- Format:

## Requirements (Must / Should / Won’t)
Must:
- ...

Should:
- ...

Won’t:
- ...

## Validation
- Tests:
- Commands:
```

Använd mallen som start och håll den kort. Specen ska minska oklarhet, inte skapa ett nytt projekt.

---

## 12) GSD som enkel start för SDD

Om du vill komma igång snabbt med SDD är GSD ett bra och enkelt alternativ i dagsläget. Det ger ett lättviktigt flöde med tydliga steg (fråga → planera → utföra → verifiera) och håller specs och validering nära själva arbetet.

Du behöver inte adoptera hela systemet för att få värde. Använd det som start och anpassa processen till teamets behov.
