# LLM
A Python script to make a call to a LLM. Supports:

- Streaming responses
- Function calling
- Saving conversations

## Prerequisites
### Packages
`pip install openai`

### Configuration

Option 1: Set environment variables directly

(For Bash)
```bash
export AZURE_OPENAI_ENDPOINT=...
export AZURE_OPENAI_API_KEY=...
```

(For PowerShell)
```powershell
$env:AZURE_OPENAI_ENDPOINT=...
$env:AZURE_OPENAI_API_KEY=...
```

Option 2: Use a JSON file

1. Create the credentials file:
```
echo '{"AZURE_OPENAI_ENDPOINT":"...","AZURE_OPENAI_API_KEY":"..."}' > credentials.json
```

2. Specify the credentials file:
```
llm.py --credentials_file credentials.json

```

Alternatively set the `LLM_CREDENTIALS_FILE` environment variable to the credentials file:

(For Bash)
```bash

export LLM_CREDENTIALS_FILE=credentials.json
```

(For PowerShell)
```powershell

$env:LLM_CREDENTIALS_FILE=credentials.json
```

## How to use
```
llm.py --help

llm.py # will prompt for a user message

llm.py --user_message "What functions can you call and what are their arguments?"

llm.py --messages messages.json --save_messages true
```

## Function calling
Supports reading files, writing files, and listing files in a directory.

```
llm.py 
User message: What functions can you call and what are their arguments?
Here are the functions I can call and their arguments:

1. **read_file**
   - **file**: The name and extension of the file to read from.

2. **write_file**
   - **file**: The name and extension of the file to write to.
   - **text**: Text to write to the file as a single string.

3. **dir**
   - **path**: Path to the folder or directory from which to get files and other metadata.
```

### Adding new functions
1. Create a new file in the `functions` folder (e.g. `functions/new_function.py`) following this format:

```python
class NewFunction:
    def function(self, arg1, arg2, ...):
        # implementation
        return result # some result is returned to the LLM

    def parse_args(self, function_args):
        return {
            "arg1": function_args.get("arg1"),
            "arg2": function_args.get("arg2"),
            ...
        }

    name = "<name of the function>"
    definition = {
        "type": "function",
        "function": {
            "name": "<name of the function>",
            "description": "<description of the function>",
            "parameters": {
                "type": "object",
                "properties": {
                    "arg1": {
                        "type": "<type of first argument e.g. string>",
                        "description": "<description of the first argument>"
                    },
                    "arg2": {
                        "type": "...",
                        "description": "..."
                    }
                },
                "required": ["arg1", ...]
            }
        }
    }

```

2. Import the new function in `functions/__init__.py` and instantiate it in the list of functions:

```python
from .new_function import NewFunction

functions = [
    ...
    NewFunction()
]
```

