import json

from .read_file import ReadFileFunction
from .write_file import WriteFileFunction
from .dir import DirFunction
from .shell import ShellFunction

functions = [
    ReadFileFunction(),
    WriteFileFunction(),
    DirFunction(),
    ShellFunction()
]

function_dictionary = {fn.name: fn for fn in functions}
available_functions = {fn.name: fn.function for fn in functions}
tools = [fn.definition for fn in functions]

def parse_args(function_name, function_args):
    if not function_name in function_dictionary:
        raise ValueError()

    return function_dictionary[function_name].parse_args(json.loads(function_args))

