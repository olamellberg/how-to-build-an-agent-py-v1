# Hur man bygger en agent (Cursor + Python)
**Version 1.0** | 2026-01-22
### eller: Kejsaren har inga kläder (och det har inte heller den här tutorialen)

Det är inte så svårt att bygga en fullt fungerande kodredigeringsagent.

Det verkar som om det skulle vara det. När man ser en agent redigera filer, köra kommandon, ta sig ur fel, prova olika strategier — det verkar som att det måste finnas en hemlighet bakom.

Det finns det inte. Det är en LLM, en loop och tillräckligt med tokens. Resten, det som gör det så beroendeframkallande och imponerande? Hårt arbete.

Men att bygga en liten och ändå mycket imponerande agent kräver inte ens det. Du kan göra det på mindre än 400 rader kod, varav det mesta är boilerplate.

Jag ska visa dig hur, just nu. Vi ska skriva lite kod tillsammans och gå från noll rader kod till "oj, det här är… en spelväxlare."

Men här blir det *konstigt*.

**Vi ska använda en agent för att bygga en agent.**

Precis så — vi ska öppna Cursor, starta dess AI-agent, och be *den* att hjälpa oss bygga vår egen AI-agent. Vi ska använda en AI-kodassistent för att bygga en AI-kodassistent. Det är rekursivt. Det är meta. Det är agenter hela vägen ner.

Om det låter som fusk, tja… kanske är det det. Men det är också poängen. Dessa verktyg är så kraftfulla nu att du kan använda dem för att bygga fler av sig själva. Och i slutet av denna tutorial kommer du att förstå exakt varför det fungerar — eftersom du kommer att se hur enkel "magin" verkligen är.

Jag *uppmanar* dig att följa med. Nej, verkligen. Du kanske tror att du bara kan läsa detta och att du inte behöver skriva ut koden, men det är mindre än 400 rader kod. Jag behöver att du *känner* hur lite kod det är och jag vill att du ser detta med dina egna ögon i din egen terminal i dina egna mappar. Och med Cursors agent som hjälper dig behöver du inte ens skriva det mesta — du *beskriver* vad du vill ha och ser det dyka upp.

## Vad vi behöver

- [Python 3.10+](https://www.python.org/)
- [OpenAI API-nyckel](https://platform.openai.com/api-keys) som du sätter som miljövariabel, `OPENAI_API_KEY`
- [Cursor IDE](https://cursor.com/) — det är här meta-magisken händer

## Ta fram pennan!

Låt oss börja med att öppna Cursor och skapa ett nytt projekt. Öppna Cursor, gå sedan till **File → Open Folder** och skapa en ny mapp som heter `code-editing-agent`.

Nu, öppna Cursors integrerade terminal med `Ctrl+` (det är backtick-tangenten). Låt oss sätta upp vår Python-miljö:

```bash
python -m venv venv
venv\Scripts\activate  # På Mac/Linux: source venv/bin/activate
pip install openai
```

Nu kommer den roliga delen. I stället för att skriva all kod själva, låt oss be Cursor om hjälp. Tryck `Ctrl+I` för att öppna agentpanelen, och ge den denna prompt:

**Prompt för Cursor:**
"Skapa en ny fil som heter agent.py med en grundläggande skeleton för en CLI-chattapplikation med OpenAI SDK. Inkludera en Agent-klass med en __init__ som tar en client och en get_user_message-funktion. Lägg till en get_user_message-funktion som läser från stdin. Inkludera en main-funktion som skapar clienten och agenten."

Cursor kommer generera något som detta:

```python
from openai import OpenAI


def get_user_message():
    try:
        return input(), True
    except EOFError:
        return "", False


class Agent:
    def __init__(self, client, get_user_message_func):
        self.client = client
        self.get_user_message = get_user_message_func


def main():
    client = OpenAI()
    agent = Agent(client, get_user_message)
    agent.run()


if __name__ == "__main__":
    main()
```

Ja, detta körs inte ännu. Men vad vi har här är en `Agent` som har tillgång till en `OpenAI`-client (som som standard letar efter `OPENAI_API_KEY`) och som kan få ett användarmeddelande genom att läsa från stdin i terminalen.

Nu låt oss lägga till den saknade `run()`-metoden. Be Cursor:

**Prompt för Cursor:**
"Lägg till en run()-metod i Agent-klassen som implementerar en chatloop. Den ska: upprätthålla en konversationslista, skriva ut en prompt för användarinput, lägga till meddelanden i konversationen, anropa run_inference för att få modellens svar, och skriva ut assistentens textsvar. Lägg också till en run_inference-metod som anropar OpenAI chat completions API med gpt-4o."

Cursor kommer uppdatera din Agent-klass så att den ser ut så här:

```python
class Agent:
    def __init__(self, client, get_user_message_func):
        self.client = client
        self.get_user_message = get_user_message_func

    def run(self):
        conversation = []
        print("Chat with the assistant (use 'ctrl-c' to quit)")

        while True:
            print("\033[94mYou\033[0m: ", end="")
            user_input, ok = self.get_user_message()
            if not ok:
                break

            conversation.append({
                "role": "user",
                "content": user_input
            })

            response = self.run_inference(conversation)
            message = response.choices[0].message
            conversation.append({
                "role": "assistant",
                "content": message.content
            })

            if message.content:
                print(f"\033[93mAssistant\033[0m: {message.content}")

    def run_inference(self, conversation):
        return self.client.chat.completions.create(
            model="gpt-4o",
            max_tokens=1024,
            messages=conversation
        )
```

Det är inte mycket, eller hur? Ungefär 40 rader och det viktigaste i dem är denna loop i `run()` som låter oss prata med modellen. Men det är redan hjärtat i detta program.

Låt oss köra det. Först, sätt din API-nyckel i terminalen:

```bash
set OPENAI_API_KEY=din-api-nyckel-här  # På Mac/Linux: export OPENAI_API_KEY=...

# Kör det
python agent.py
```

Sedan kan du bara prata med assistenten, så här:

```
$ python agent.py
Chat with the assistant (use 'ctrl-c' to quit)
You: Hej! Jag bygger en agent! Hur mår du?
Assistant: Hej! Det är spännande - att bygga en agent är ett bra sätt att förstå hur AI-system fungerar under huven. Jag mår bra, tack för att du frågade. Hur går ditt agentprojekt hittills? Vilken typ av funktioner planerar du att ge den?
You:
```

Lägg märke till hur vi höll samma konversation igång över flera varv. `conversation` växer längre med varje varv och vi skickar hela konversationen varje gång. Servern — OpenAIs server — är tillståndslös. Den ser bara vad som finns i `conversation`-listan. Det är upp till oss att upprätthålla det.

Okej, låt oss gå vidare, eftersom detta inte är en agent ännu. Vad är en agent? En agent är en loop där en LLM planerar, anropar verktyg, läser resultat och upprepar tills uppgiften är klar. Den viktigaste insikten ([diskuteras här](https://youtu.be/J1-W9O3n7j8?t=72)) är att verktyg ger LLM:en möjligheten att modifiera något utanför kontextfönstret — det är det som gör det till en *agent* snarare än bara en chatbot.

## Ett första verktyg

En LLM med *åtkomst till verktyg*? Vad är ett verktyg? Grundidén är denna: du skickar en prompt till modellen som säger att den ska svara på ett visst sätt om den vill använda "ett verktyg". Sedan, som mottagare av det meddelandet, "använder du verktyget" genom att köra det och svara med resultatet. Det är allt. Allt annat vi kommer att se är bara abstraktion ovanpå det.

För att sammanfatta, allt som finns till verktyg och verktygsanvändning är två saker:

1. Du berättar för modellen vilka verktyg som finns tillgängliga
2. När modellen vill köra verktyget, berättar den för dig, du kör verktyget och skickar svaret upp

För att göra (1) enklare har de stora modellleverantörerna inbyggda API:er för att skicka verktygsdefinitioner tillsammans.

Okej, nu låt oss bygga vårt första verktyg: `read_file`

## Verktyget `read_file`

Varje verktyg vi kommer att lägga till kommer att kräva följande:

- Ett namn
- En beskrivning för att berätta för modellen vad verktyget gör, när det ska användas, när det inte ska användas, vad det returnerar och så vidare
- Ett input-schema som beskriver, som ett JSON-schema, vilka inputs detta verktyg förväntar sig och i vilken form
- En funktion som faktiskt kör verktyget med inputen modellen skickar till oss och returnerar resultatet

Låt oss be Cursor att sätta upp verktygsinfrastrukturen. Tryck `Ctrl+I` och ange:

**Prompt för Cursor:**
"Lägg till en ToolDefinition dataclass med fält: name (str), description (str), input_schema (dict), och function (Callable). Uppdatera Agent __init__ för att acceptera en valfri tools-parameter. Uppdatera run_inference för att konvertera verktygsdefinitioner till OpenAIs format och skicka dem till API-anropet."

Cursor kommer lägga till något som detta:

```python
from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class ToolDefinition:
    name: str
    description: str
    input_schema: dict
    function: Callable[[dict], str]
```

Och uppdatera Agent-klassen:

```python
class Agent:
    # `tools` läggs till här:
    def __init__(self, client, get_user_message_func, tools=None):
        self.client = client
        self.get_user_message = get_user_message_func
        self.tools = tools or []

    def run_inference(self, conversation):
        # Konvertera våra verktygsdefinitioner till OpenAIs format
        openai_tools = [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.input_schema,
                }
            }
            for tool in self.tools
        ]

        return self.client.chat.completions.create(
            model="gpt-4o",
            max_tokens=1024,
            messages=conversation,
            tools=openai_tools if openai_tools else None
        )
```

Nu låt oss skapa det faktiska `read_file`-verktyget. Be Cursor:

**Prompt för Cursor:**
"Skapa ett read_file-verktyg. Funktionen ska ta en dict med 'path' och läsa filen. Skapa en ToolDefinition med namn 'read_file', en beskrivning som förklarar när det ska användas, ett JSON-schema för input med en 'path'-egenskap, och funktionen. Uppdatera main() för att skicka verktyget till Agent."

Cursor kommer skapa något som detta:

```python
def read_file(input_data: dict) -> str:
    """Read the contents of a file at the given path."""
    path = input_data["path"]
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error: {str(e)}"


READ_FILE_TOOL = ToolDefinition(
    name="read_file",
    description="Read the contents of a given relative file path. Use this when you want to see what's inside a file. Do not use this with directory names.",
    input_schema={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The relative path of a file in the working directory."
            }
        },
        "required": ["path"]
    },
    function=read_file
)
```

Och uppdatera `main()`:

```python
def main():
    client = OpenAI()
    tools = [READ_FILE_TOOL]
    agent = Agent(client, get_user_message, tools)
    agent.run()
```

Men vi behöver också uppdatera `run()`-metoden för att hantera verktygsanrop. Be Cursor:

**Prompt för Cursor:**
"Uppdatera run()-metoden för att hantera tool_use i modellens svar. När modellen vill använda ett verktyg, kör funktionen, lägg till resultatet i konversationen, och skicka tillbaka till modellen för att få det slutliga svaret."

Cursor kommer uppdatera `run()` så att den hanterar verktygsanrop korrekt. Nu har du en fungerande agent som kan läsa filer!

## Ytterligare verktyg: list_files och edit_file

Med samma mönster kan du lägga till fler verktyg:

- `list_files` — lista filer i en katalog
- `edit_file` — redigera en fil genom att ersätta gammal text med ny text

Varje verktyg följer samma mönster: en funktion, en ToolDefinition, och läggs till i tools-listan.

## Slutsats

Det är inte så svårt. En agent är bara:
- En LLM
- En loop
- Verktyg
- Tillräckligt med tokens

Resten är bara detaljer och boilerplate. Men dessa detaljer — hur du strukturerar verktygen, hur du hanterar fel, hur du designar feedback-loopen — det är där skillnaden mellan en demo och något användbart ligger.

### Produktionsfallgropar (vad som går sönder efter demon)
När du går från “cool prototyp” till “användbart verktyg” skiftar felen:

- **Konceptuella fel > syntaxfel**: agenten kan producera plausibel kod som är fel för dina verkliga constraints. Gör framgångskriterier och invarianter explicita.
- **Antaganden måste vara synliga**: lägg till ett `assumptions`/`unknowns`-fält (eller motsvarande) i agentens output, bredvid `verification_steps`.
- **Bloat-kontroll spelar roll**: håll scopet tajt, föredra minsta diff, och ta bort död kod under refaktoreringar i stället för att lämna parallella vägar bakom dig.
- **Verifiering är en produktfeature**: investera i en harness (ett-kommando-check), riktade tester och lättviktiga evals så att du kan iterera säkert.

**Och det roligaste?** Du kan använda Cursor för att bygga allt detta. Det är rekursivt. Det är meta. Det är agenter hela vägen ner.
