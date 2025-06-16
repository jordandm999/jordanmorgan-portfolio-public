print("LOADING MCP SERVER")
from fastapi import FastAPI, Request
from mcp.server.sse import SseServerTransport
from mcp.server.fastmcp import FastMCP
from starlette.routing import Mount
from .tools import tool_registry

# Create FastAPI app
app = FastAPI()

# Set up SSE transport
sse_transport = SseServerTransport("/mcp_server/messages/")
app.router.routes.append(Mount("/mcp_server/messages", app=sse_transport.handle_post_message))

# Initialize MCP
mcp = FastMCP()
for tool in tool_registry:
    mcp.tool()(tool)

# Root endpoint handler for MCP server
@app.route("/mcp_server", methods=["GET", "POST"])
async def handle_mcp_root(request: Request):
    if request.method == "GET":
        # For GET requests, treat it as an SSE connection
        async with sse_transport.connect_sse(request.scope, request.receive, request._send) as (read_stream, write_stream):
            await mcp._mcp_server.run(
                read_stream,
                write_stream,
                mcp._mcp_server.create_initialization_options(),
            )
    else:
        # For POST requests, handle as a message
        return await sse_transport.handle_post_message(request)
    return

# List available tools
@app.get("/mcp_server/list_tools")
def list_tools():
    tools = []
    for func in tool_registry:
        print("FUNC:", func)
        tools.append({
            "name": func.__name__,
            "description": func.__doc__ or "",
            "parameters": [(k, str(v)) for k, v in func.__annotations__.items()]
        })
    print("TOOLS:", tools)
    return tools