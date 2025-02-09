import subprocess

class SqliteScriptRunFunction:
    def function(self, db, script):
        result = subprocess.run(["sqlite3", "-init", script, db], input=".quit", capture_output=True, text=True)
        return result.returncode == 0

    def parse_args(self, function_args):
        return {
            "db": function_args.get("db"),
            "script": function_args.get("script")
        }

    name = "sqlite_script_run"
    definition = {
        "type": "function",
        "function": {
            "name": "sqlite_script_run",
            "description": "Run a SQL script against a sqlite database and returns whether the command was successful",
            "parameters": {
                "type": "object",
                "properties": {
                    "db": {
                        "type": "string",
                        "description": "Path to the sqlite database file"
                    },
                    "script": {
                        "type": "string",
                        "description": "Path to the SQL script to run in the sqlite database"
                    }
                },
                "required": ["db", "script"]
            }
        }
    }

