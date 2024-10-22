import os

class DirFunction:
    def function(self, path):
        result = os.listdir(path)
        return result

    def parse_args(self, function_args):
        return {
            "path": function_args.get("path")
        }

    name = "dir"
    definition = {
        "type": "function",
        "function": {
            "name": "dir",
            "description": "Get list of files and folders of a path",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to folder or directory which to get files and other metadata"
                    }
                },
                "required": ["path"]
            }
        }
    }
