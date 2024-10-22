
class ReadFileFunction:
    def function(self, file):
        try:
            file = open(file, 'r', encoding="utf-8")
            contents = file.read()
            file.close()
            return contents
        except:
            return None

    def parse_args(self, function_args):
        return {
            "file": function_args.get("file")
        }

    name = "read_file"
    definition = {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read text from a file and return the contents",
            "parameters": {
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "description": "Name and extension of the file to read from"
                    }
                },
                "required": ["file"]
            }
        }
    }

