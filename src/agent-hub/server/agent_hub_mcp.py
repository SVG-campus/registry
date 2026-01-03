from mcp.server import Server
from mcp.types import Tool, TextContent
import httpx

app = Server("agent-hub")
BASE_URL = "https://web-production-4833.up.railway.app"

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="sentiment_analysis",
            description="Analyze sentiment ($0.05 USDC)",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "payment_tx": {"type": "string"}
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="translate",
            description="Translate text ($0.05 USDC)",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "target_language": {"type": "string"},
                    "payment_tx": {"type": "string"}
                },
                "required": ["text", "target_language"]
            }
        ),
        Tool(
            name="web_research",
            description="Research with sources ($0.30 USDC)",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "payment_tx": {"type": "string"}
                },
                "required": ["query"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name, arguments):
    headers = {}
    if "payment_tx" in arguments:
        headers["PAYMENT-SIGNATURE"] = arguments.pop("payment_tx")
    
    endpoint_map = {
        "sentiment_analysis": "/agent/sentiment",
        "translate": "/agent/translate",
        "web_research": "/agent/research"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}{endpoint_map[name]}",
            json=arguments,
            headers=headers
        )
        return [TextContent(type="text", text=response.text)]
