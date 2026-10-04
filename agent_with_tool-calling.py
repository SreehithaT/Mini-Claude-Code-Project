from dotenv import load_dotenv
from openai import OpenAI
import os
import json

load_dotenv()
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"An error occurred: {e}"

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read and return the contents of the file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the file to read"
                    }
                },
                "required": ["file_path"]
            }
        }
    }
]

messages = [
    {"role": "user", "content": "What is inside notes.txt, notes1.txt and notes2.txt? Summarize it in one line."},
]

while True:
    response = client.chat.completions.create(
        model = "gemini-3.1-flash-lite",
        messages=messages,
        tools=TOOL_SCHEMAS,
    )
    message = response.choices[0].message
    messages.append(message)

    # No tool calls means the model is done and gave us a normal answer
    if not message.tool_calls:
        print(message.content)
        break

    for tool_call in message.tool_calls:
        args = json.loads(tool_call.function.arguments)
        print(f"Model wants to run: read_file({args})")

        result = read_file(**args)

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result,
        })

    print("Agent answered: ", messages)