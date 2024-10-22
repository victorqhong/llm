import subprocess

class ShellFunction:
    def function(self, command):
        result = subprocess.run(command.split(" "), capture_output=True, text=True)
        return { "returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr }

    def parse_args(self, function_args):
        return {
            "command": function_args.get("command")
        }

    name = "shell"
    definition = {
        "type": "function",
        "function": {
            "name": "shell",
            "description": "Runs a shell command",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Shell command and arguments to run"
                    }
                },
                "required": ["command"]
            }
        }
    }
