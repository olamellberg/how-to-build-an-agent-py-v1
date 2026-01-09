"""
A simple code-editing agent in Python.

This is a complete, working implementation of the agent described in
"How to Build an Agent" - Python Edition.

Requirements:
    pip install anthropic

Usage:
    export ANTHROPIC_API_KEY="your-api-key"
    python agent.py
"""

import anthropic
import json
import os
from dataclasses import dataclass
from typing import Callable


@dataclass
class ToolDefinition:
    """A tool that Claude can use."""
    name: str
    description: str
    input_schema: dict
    function: Callable[[dict], str]


# =============================================================================
# Tool: read_file
# =============================================================================

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
    description="""Read the contents of a given relative file path. Use this when you want to see what's inside a file. Do not use this with directory names.""",
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


# =============================================================================
# Tool: list_files
# =============================================================================

def list_files(input_data: dict) -> str:
    """List files and directories at a given path."""
    path = input_data.get("path", ".")

    try:
        files = []
        for root, dirs, filenames in os.walk(path):
            for d in dirs:
                rel_path = os.path.relpath(os.path.join(root, d), path)
                files.append(rel_path + "/")
            for f in filenames:
                rel_path = os.path.relpath(os.path.join(root, f), path)
                files.append(rel_path)
        return json.dumps(files)
    except Exception as e:
        return f"Error: {str(e)}"


LIST_FILES_TOOL = ToolDefinition(
    name="list_files",
    description="""List files and directories at a given path. If no path is provided, lists files in the current directory.""",
    input_schema={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Optional relative path to list files from. Defaults to current directory if not provided."
            }
        }
    },
    function=list_files
)


# =============================================================================
# Tool: edit_file
# =============================================================================

def create_new_file(path: str, content: str) -> str:
    """Create a new file with the given content."""
    try:
        # Create directories if they don't exist
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(path, "w") as f:
            f.write(content)

        return f"Successfully created file {path}"
    except Exception as e:
        return f"Error: {str(e)}"


def edit_file(input_data: dict) -> str:
    """Edit a file by replacing old_str with new_str."""
    path = input_data["path"]
    old_str = input_data["old_str"]
    new_str = input_data["new_str"]

    if not path or old_str == new_str:
        return "Error: invalid input parameters"

    # If file doesn't exist and old_str is empty, create new file
    if not os.path.exists(path) and old_str == "":
        return create_new_file(path, new_str)

    try:
        with open(path, "r") as f:
            content = f.read()

        if old_str and old_str not in content:
            return "Error: old_str not found in file"

        new_content = content.replace(old_str, new_str)

        with open(path, "w") as f:
            f.write(new_content)

        return "OK"

    except Exception as e:
        return f"Error: {str(e)}"


EDIT_FILE_TOOL = ToolDefinition(
    name="edit_file",
    description="""Make edits to a text file. Replaces 'old_str' with 'new_str' in the given file.
'old_str' and 'new_str' MUST be different from each other.

If the file specified with path doesn't exist, it will be created.""",
    input_schema={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The path to the file"
            },
            "old_str": {
                "type": "string",
                "description": "Text to search for - must match exactly and must only have one match exactly"
            },
            "new_str": {
                "type": "string",
                "description": "Text to replace old_str with"
            }
        },
        "required": ["path", "old_str", "new_str"]
    },
    function=edit_file
)


# =============================================================================
# Agent
# =============================================================================

class Agent:
    """A simple agent that can chat with Claude and use tools."""

    def __init__(self, client, get_user_message_func, tools=None):
        self.client = client
        self.get_user_message = get_user_message_func
        self.tools = tools or []

    def run(self):
        """Main loop: chat with the user and execute tools as needed."""
        conversation = []
        print("Chat with Claude (use 'ctrl-c' to quit)")

        read_user_input = True

        while True:
            if read_user_input:
                print("\033[94mYou\033[0m: ", end="")
                user_input, ok = self.get_user_message()
                if not ok:
                    break
                conversation.append({
                    "role": "user",
                    "content": user_input
                })

            message = self.run_inference(conversation)
            conversation.append({
                "role": "assistant",
                "content": message.content
            })

            tool_results = []
            for block in message.content:
                if block.type == "text":
                    print(f"\033[93mClaude\033[0m: {block.text}")
                elif block.type == "tool_use":
                    result = self.execute_tool(block.id, block.name, block.input)
                    tool_results.append(result)

            if not tool_results:
                read_user_input = True
                continue

            read_user_input = False
            conversation.append({
                "role": "user",
                "content": tool_results
            })

    def run_inference(self, conversation):
        """Send the conversation to Claude and get a response."""
        # Convert our tool definitions to Anthropic's format
        anthropic_tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.input_schema,
            }
            for tool in self.tools
        ]

        return self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=conversation,
            tools=anthropic_tools if anthropic_tools else []
        )

    def execute_tool(self, tool_id, name, tool_input):
        """Execute a tool and return the result."""
        # Find the tool
        tool = next((t for t in self.tools if t.name == name), None)
        if not tool:
            return {
                "type": "tool_result",
                "tool_use_id": tool_id,
                "content": "Tool not found",
                "is_error": True
            }

        print(f"\033[92mtool\033[0m: {name}({json.dumps(tool_input)})")

        try:
            result = tool.function(tool_input)
            return {
                "type": "tool_result",
                "tool_use_id": tool_id,
                "content": result
            }
        except Exception as e:
            return {
                "type": "tool_result",
                "tool_use_id": tool_id,
                "content": str(e),
                "is_error": True
            }


# =============================================================================
# Main
# =============================================================================

def get_user_message():
    """Read a line of input from the user."""
    try:
        return input(), True
    except EOFError:
        return "", False


def main():
    """Entry point: create the agent and run it."""
    client = anthropic.Anthropic()
    tools = [READ_FILE_TOOL, LIST_FILES_TOOL, EDIT_FILE_TOOL]
    agent = Agent(client, get_user_message, tools)
    agent.run()


if __name__ == "__main__":
    main()
