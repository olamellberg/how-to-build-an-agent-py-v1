# How to Build an Agent (Cursor + Python Edition)
**Version 1.0** | 2026-01-22
### or: The Emperor Has No Clothes (And Neither Does This Tutorial)

It's not that hard to build a fully functioning, code-editing agent.

It seems like it would be. When you look at an agent editing files, running commands, wriggling itself out of errors, retrying different strategies — it seems like there has to be a secret behind it.

There isn't. It's an LLM, a loop, and enough tokens. The rest, the stuff that makes it so addictive and impressive? Elbow grease.

But building a small and yet highly impressive agent doesn't even require that. You can do it in less than 400 lines of code, most of which is boilerplate.

I'm going to show you how, right now. We're going to write some code together and go from zero lines of code to "oh wow, this is… a game changer."

But here's where it gets *weird*.

**We're going to use an agent to build an agent.**

That's right — we're going to open Cursor, fire up its AI agent, and ask *it* to help us build our own AI agent. We're going to use an AI coding assistant to build an AI coding assistant. It's recursive. It's meta. It's agents all the way down.

If that sounds like cheating, well… maybe it is. But it's also the point. These tools are so powerful now that you can use them to build more of themselves. And by the end of this tutorial, you'll understand exactly why that works — because you'll see how simple the "magic" really is.

I *urge* you to follow along. No, really. You might think you can just read this and that you don't have to type out the code, but it's less than 400 lines of code. I need you to *feel* how little code it is and I want you to see this with your own eyes in your own terminal in your own folders. And with Cursor's agent helping you, you won't even have to type most of it — you'll *describe* what you want and watch it appear.

## What we need

- [Python 3.10+](https://www.python.org/)
- [OpenAI API key](https://platform.openai.com/api-keys) that you set as an environment variable, `OPENAI_API_KEY`
- [Cursor IDE](https://cursor.com/) — this is where the meta-magic happens

## Pencils out!

Let's start by opening Cursor and creating a new project. Open Cursor, then go to **File → Open Folder** and create a new folder called `code-editing-agent`.

Now, open Cursor's integrated terminal with `Ctrl+` (that's the backtick key). Let's set up our Python environment:

```bash
python -m venv venv
venv\Scripts\activate  # On Mac/Linux: source venv/bin/activate
pip install openai
```

Now comes the fun part. Instead of typing all the code ourselves, let's ask Cursor to help. Press `Ctrl+I` to open the agent panel, and give it this prompt:

**Prompt for Cursor:**
"Create a new file called agent.py with a basic skeleton for a CLI chat application using the OpenAI SDK. Include an Agent class with an __init__ that takes a client and a get_user_message function. Add a get_user_message function that reads from stdin. Include a main function that creates the client and agent."

Cursor will generate something like this:

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

Yes, this doesn't run yet. But what we have here is an `Agent` that has access to an `OpenAI` client (which, by default, looks for `OPENAI_API_KEY`) and that can get a user message by reading from stdin on the terminal.

Now let's add the missing `run()` method. Ask Cursor:

**Prompt for Cursor:**
"Add a run() method to the Agent class that implements a chat loop. It should: maintain a conversation list, print a prompt for user input, append messages to the conversation, call run_inference to get the model's response, and print the assistant's text responses. Also add a run_inference method that calls the OpenAI chat completions API with gpt-4o."

Cursor will update your Agent class to look like this:

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

It's not a lot, is it? About 40 lines and the most important thing in them is this loop in `run()` that lets us talk to the model. But that's already the heartbeat of this program.

Let's run it. First, set your API key in the terminal:

```bash
set OPENAI_API_KEY=your-api-key-here  # On Mac/Linux: export OPENAI_API_KEY=...

# Run it
python agent.py
```

Then you can just talk to the assistant, like this:

```
$ python agent.py
Chat with the assistant (use 'ctrl-c' to quit)
You: Hey! I'm building an agent! How are you?
Assistant: Hi! That's exciting - building an agent is a great way to understand how AI systems work under the hood. I'm doing well, thanks for asking. How's your agent project going so far? What kind of capabilities are you planning to give it?
You:
```

Notice how we kept the same conversation going over multiple turns. The `conversation` grows longer with every turn and we send the whole conversation every time. The server — OpenAI's server — is stateless. It only sees what's in the `conversation` list. It's up to us to maintain that.

Okay, let's move on, because this is not an agent yet. What's an agent? An agent is a loop where an LLM plans, calls tools, reads results, and repeats until the task is complete. The key insight ([discussed here](https://youtu.be/J1-W9O3n7j8?t=72)) is that tools give the LLM the ability to modify something outside the context window — that's what makes it an *agent* rather than just a chatbot.

## A First Tool

An LLM with *access to tools*? What's a tool? The basic idea is this: you send a prompt to the model that says it should reply in a certain way if it wants to use "a tool". Then you, as the receiver of that message, "use the tool" by executing it and replying with the result. That's it. Everything else we'll see is just abstraction on top of it.

To summarize, all there is to tools and tool use are two things:

1. You tell the model what tools are available
2. When the model wants to execute the tool, it tells you, you execute the tool and send the response up

To make (1) easier, the big model providers have built-in APIs to send tool definitions along.

Okay, now let's build our first tool: `read_file`

## The `read_file` tool

Each tool we're going to add will require the following:

- A name
- A description to tell the model what the tool does, when to use it, when to not use it, what it returns and so on
- An input schema that describes, as a JSON schema, what inputs this tool expects and in which form
- A function that actually executes the tool with the input the model sends to us and returns the result

Let's ask Cursor to set up the tool infrastructure. Press `Ctrl+I` and enter:

**Prompt for Cursor:**
"Add a ToolDefinition dataclass with fields: name (str), description (str), input_schema (dict), and function (Callable). Update the Agent __init__ to accept an optional tools parameter. Update run_inference to convert tool definitions to OpenAI's format and pass them to the API call."

Cursor will add something like this:

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

And update the Agent class:

```python
class Agent:
    # `tools` is added here:
    def __init__(self, client, get_user_message_func, tools=None):
        self.client = client
        self.get_user_message = get_user_message_func
        self.tools = tools or []

    def run_inference(self, conversation):
        # Convert our tool definitions to OpenAI's format
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

Now let's create the actual `read_file` tool. Ask Cursor:

**Prompt for Cursor:**
"Create a read_file tool. The function should take a dict with 'path' and read the file. Create a ToolDefinition with name 'read_file', a description explaining when to use it, a JSON schema for input with a 'path' property, and the function. Update main() to pass the tool to Agent."

Cursor will create something like this:

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

And update `main()`:

```python
def main():
    client = OpenAI()
    tools = [READ_FILE_TOOL]
    agent = Agent(client, get_user_message, tools)
    agent.run()
```

But we also need to update the `run()` method to handle tool calls. Ask Cursor:

**Prompt for Cursor:**
"Update the run() method to handle tool_use in the model's response. When the model wants to use a tool, execute the function, add the result to the conversation, and send back to the model to get the final answer."

Cursor will update `run()` to handle tool calls correctly. Now you have a working agent that can read files!

## Additional tools: list_files and edit_file

With the same pattern, you can add more tools:

- `list_files` — list files in a directory
- `edit_file` — edit a file by replacing old text with new text

Each tool follows the same pattern: a function, a ToolDefinition, and added to the tools list.

## Conclusion

It's not that hard. An agent is just:
- An LLM
- A loop
- Tools
- Enough tokens

The rest is just details and boilerplate. But those details — how you structure the tools, how you handle errors, how you design the feedback loop — that's where the difference between a demo and something useful lies.

**And the funniest part?** You can use Cursor to build all of this. It's recursive. It's meta. It's agents all the way down.
