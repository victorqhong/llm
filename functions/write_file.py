class WriteFileFunction:
    def function(self, file, text):
        file = open(file, 'w')
        file.write(text)
        file.flush()
        file.close()
        return True

    def parse_args(self, function_args):
        return {
            "file": function_args.get("file"),
            "text": function_args.get("text"),
        }

    name = "write_file"
    definition = {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write text to a file and return True or False depending if the result was successful",
            "parameters": {
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "description": "Name and extension of the file to write to"
                    },
                    "text": {
                        "type": "string",
                        "description": "Text to write to the file as a single string"
                    }
                },
                "required": ["file", "text"]
            }
        }
    }

