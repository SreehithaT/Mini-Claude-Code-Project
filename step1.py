from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

#gnerating response here. Only thing an LLm does is generate text. It does not call the tool/ doesn't go save a memory/ doesn't go to web and research something.
#you give in some tokens and it gives out some tokens.

'''
How do we train this LLM to turn out as an Agent?
We will send multiple requests to API and we will ask model what to do with tools.
'''
response = client.chat.completions.create(
    model = "gemini-3.8-flash",
    messages=[{"role": "user", "content": "Explain what an AI agent is"},
    ],
)

print(response.choices[0].message.content)