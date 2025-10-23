from mcp_openai import MCPClient
from mcp_openai import config
import os 
from dotenv import load_dotenv
import asyncio
import random 


load_dotenv()


mcp_client_config = config.MCPClientConfig(
    mcpServers={
        "test-server": config.MCPServerConfig(
            command="uv",
            args=["run", "/home/nik/llama-mcp/mcp-openai-server/server.py"],
        )
        # add here other servers ...
    }
)

llm_client_config = config.LLMClientConfig(
    api_key="api-key-for-auth",
    base_url="http://localhost:8000/v1",
)

llm_request_config = config.LLMRequestConfig(model=os.environ["MODEL_NAME"])

client = MCPClient(
    mcp_client_config,
    llm_client_config,
    llm_request_config,
)



class TestServer:
    """Test suite for calculator operations"""
    async def test_addition(self, client):
        a, b = random.randint(1, 400), random.randint(1, 400)
        messages = [{"role": "user", "content": f"What is {a} + {b}?"}]
        messages = await client.process_messages(messages)
        response = messages[-1]["content"]
        assert str(a + b) in response
        assert len(messages) == 4

    async def test_subtraction(self, client):
        a, b = random.randint(1, 400), random.randint(1, 400)
        messages = [{"role": "user", "content": f"What is {a} - {b}?"}]
        messages = await client.process_messages(messages)
        response = messages[-1]["content"]
        assert str(a - b) in response
        assert len(messages) == 4

    async def test_multiplication(self, client):
        a, b = random.randint(1, 9), random.randint(1, 9)
        messages = [{"role": "user", "content": f"What is {a} × {b}?"}]
        messages = await client.process_messages(messages)
        response = messages[-1]["content"]
        assert str(a * b) in response
        assert len(messages) == 4

    async def test_division(self, client):
        a, b = random.randint(2, 400), random.randint(1, 400)
        messages = [{"role": "user", "content": f"What is {a * b} ÷ {b}?"}]
        messages = await client.process_messages(messages)
        response = messages[-1]["content"]
        assert str(a) in response
        assert len(messages) == 4

    async def test_all_operations(self, client):
        a, b = random.randint(1, 400), random.randint(1, 400)
        content = (
            f"What is {a} + {b}?",
            f"What is {a} - {b}?",
            f"What is {a} × {b}?",
            f"What is {a * b} ÷ {b}?",
        )
        messages = [{"role": "user", "content": "\n".join(content)}]
        messages = await client.process_messages(messages)
        msg = messages[-1]
        if "content" in msg:
            response = msg["content"]
        elif "tool_call" in msg:
            response = msg["tool_call"]["arguments"].get("result")
        else:
            response = ""
        assert str(a + b) in response
        assert str(a - b) in response
        assert str(a * b) in response
        assert str(a) in response
        assert len(messages) == 7

    # @pytest.mark.skip(reason="Not implemented")
    async def test_nested_operations(self, client):
        a, b, c = random.randint(40, 60), random.randint(40, 60), random.randint(2, 5)
        messages = [
            {
                "role": "system",
                "content": (
                    "Solve the expression step by step, following the order of "
                    "operations (PEMDAS). Solve one step at a time. Use **only** "
                    "one function at a time between `add`, `sub`, `mul` and `div`."
                ),
            },
            {"role": "user", "content": f"What is ({a} + {b}) × {c}?"},
        ]
        messages = await client.process_messages(messages)
        print("LEN MESSAGES", len(messages))

        from pprint import pprint

        pprint(messages)

        response = messages[-1]["content"]
        assert str((a + b) * c) in response
        assert len(messages) == 8

async def chat_loop():
    await client.connect_to_server("test-server")
    testServ = TestServer()
    await testServ.test_all_operations(client)

asyncio.run(chat_loop())