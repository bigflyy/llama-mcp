from openai import OpenAI
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionToolParam,
)

# connect to local llama server
client = OpenAI(base_url="http://localhost:8000/v1", api_key="")

# define tools properly
tools = [
    ChatCompletionToolParam(
        type="function",
        function={
            "name": "UserDetail",
            "parameters": {
                "type": "object",
                "title": "UserDetail",
                "properties": {
                    "name": {"title": "Name", "type": "string"},
                    "age": {"title": "Age", "type": "integer"}
                },
                "required": ["name", "age"]
            }
        }
    )
]

# messages need role + content
messages = [
    ChatCompletionUserMessageParam(
        role="user",
        content="Extract Jason is 25 years old"
    )
]

# call chat completion
completion = client.chat.completions.create(
    model="llama-3",  # your server’s exposed model name
    messages=messages,
    tools=tools,
    tool_choice={"type": "function", "function": {"name": "UserDetail"}},
    max_tokens=50
)

print(completion.choices[0].message)
