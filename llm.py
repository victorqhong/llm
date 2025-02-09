#!/usr/bin/env python3

import argparse
import json
import os

from prompt_toolkit import prompt

from openai import AzureOpenAI
from chat import Chat

azure_openai_endpoint = "AZURE_OPENAI_ENDPOINT"
azure_openai_api_key = "AZURE_OPENAI_API_KEY"

parser = argparse.ArgumentParser(prog="llm.py", description="LLM script")
parser.add_argument("--messages", type=str, default="messages.json", help="Path to json file of messages")
parser.add_argument("--save_messages", type=bool, default=False, help="Whether to save messages of this conversation")
parser.add_argument("--user_message", type=str, default="", help="User content to use")
parser.add_argument("--model_name", type=str, default="gpt-4o", help="Name of the model to use")
parser.add_argument("--credentials_file", type=str, default=os.getenv("LLM_CREDENTIALS_FILE", "credentials.json"), help="Path to JSON file with Azure OpenAI configuration. Uses LLM_CREDENTIALS_FILE environment variable by default.")

args = parser.parse_args()

azure_endpoint = os.getenv(azure_openai_endpoint) or ""
api_key = os.getenv(azure_openai_api_key)

if not azure_endpoint or not api_key:
    try:
        file = open(args.credentials_file, "r", encoding="utf-8")
        contents = file.read()
        file.close()
        credentials = json.loads(contents)

        if not azure_endpoint:
            azure_endpoint = credentials[azure_openai_endpoint]

        if not api_key:
            api_key = credentials[azure_openai_api_key]
    except:
        pass

if not azure_endpoint:
    print(f"{azure_openai_endpoint} not defined")
    exit(1)

if not api_key:
    print(f"{azure_openai_api_key} not defined")
    exit(2)

client = AzureOpenAI(
  azure_endpoint = azure_endpoint,
  api_key=api_key,
  api_version="2023-03-15-preview"
)

chat = Chat(client)

user_content = args.user_message
if user_content == "":
    try:
        user_content = prompt("User message: ", multiline=True)
    except:
        print()
        quit(3)

messages = []
messages_file = args.messages
if messages_file:
    try:
        file = open(messages_file, "r", encoding="utf-8")
        contents = file.read()
        file.close()
        messages = json.loads(contents)
    except:
        pass

chat.ask_question(user_content, messages, args.model_name)
print()

if args.save_messages:
    file = open(messages_file, 'w')
    file.write(json.dumps(messages))
    file.flush()
    file.close()

quit()

