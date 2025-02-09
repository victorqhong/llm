import subprocess

class SqliteStatementRunFunction:
    def function(self, db, statement):
        result = subprocess.run(["sqlite3", db, statement], input=".quit", capture_output=True, text=True)
        return { "returncode": result.returncode, "output": result.stdout }

    def parse_args(self, function_args):
        return {
            "db": function_args.get("db"),
            "statement": function_args.get("statement")
        }

    name = "sqlite_statement_run"
    definition = {
        "type": "function",
        "function": {
            "name": "sqlite_statement_run",
            "description": "Run a SQL statement against a sqlite database and returns whether the command was successful",
            "parameters": {
                "type": "object",
                "properties": {
                    "db": {
                        "type": "string",
                        "description": "Path to the sqlite database file"
                    },
                    "statement": {
                        "type": "string",
                        "description": "SQL statement to run in the sqlite database"
                    }
                },
                "required": ["db", "statement"]
            }
        }
    }

