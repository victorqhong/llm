from functions import tools, available_functions, parse_args

class Chat:
    def __init__(self, client):
        self.client = client

    def create_chat_completion(self, messages, model, tools = tools, tool_choice = "auto"):
        return self.client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            stream=True
        )

    def parse_chat_completion(self, completion, print_message_chunks = True):
        text_content = ""
        tool_call_chunks = {}
        tool_call_ids = {}
        for chunk in completion:
            choice = chunk.choices[0]
            if choice.delta.content:
                text_content += choice.delta.content
                if print_message_chunks:
                    print(choice.delta.content, end='', flush=True)
            if not choice.delta.tool_calls:
                continue
            for tool_call_chunk in choice.delta.tool_calls:
                if not tool_call_chunk.index in tool_call_chunks:
                    tool_call_chunks[tool_call_chunk.index] = []
                    tool_call_ids[tool_call_chunk.index] = tool_call_chunk.id
                tool_call_chunks[tool_call_chunk.index].append(tool_call_chunk.function)

        tool_calls = []
        for tool_call_index in tool_call_chunks:
            name = None
            arguments = ""
            for tool_call_chunk in tool_call_chunks[tool_call_index]:
                if name == None and tool_call_chunk.name != None:
                    name = tool_call_chunk.name
                arguments += tool_call_chunk.arguments
            tool_calls.append({
                "id": tool_call_ids[tool_call_index],
                "type": "function",
                "function": {
                    "name": name,
                    "arguments": arguments,
                }
            })

        return (text_content, tool_calls)

    def handle_chat_completion(self, messages, model):
        response = self.create_chat_completion(messages, model)
        (response_message, tool_calls) = self.parse_chat_completion(response)
        assistant_message = {
            "role": "assistant",
            "content": response_message
        }
        if len(tool_calls) > 0:
            assistant_message["tool_calls"] = tool_calls
        messages.append(assistant_message)
        for tool_call in tool_calls:
            function_name = tool_call["function"]["name"]
            function_args = tool_call["function"]["arguments"]
            kwargs = parse_args(function_name, function_args)
            function_to_call = available_functions[function_name]
            function_response = function_to_call(**kwargs)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "name": function_name,
                "content": str(function_response),
            })
        if len(tool_calls) > 0:
            self.handle_chat_completion(messages, model)

    def ask_question(self, user_content, messages, model = "gpt-4o"):
        messages.append({
            "role": "user",
            "content": user_content
        })
        self.handle_chat_completion(messages, model)

    def generate_tool_call(self, id, name, arguments):
        return {
            "id": id,
            "type": "function",
            "function": {
                "name": name,
                "arguments": arguments
            }
        }
