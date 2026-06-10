"""
PPTX Extractor — MCP Server
Exposes a single tool: extract_pptx(file_base64, filename)
Run locally and expose via Microsoft Dev Tunnel.
"""

import base64
import json
import logging

from mcp.server.fastmcp import FastMCP
from extractor import extract_pptx

logging.basicConfig(level=logging.INFO)

mcp = FastMCP(
    name="pptx-extractor",
    instructions=(
        "Use extract_pptx to extract structured content (titles, text, tables) "
        "from a PowerPoint (.pptx) file. Pass the file as a base64-encoded string."
    ),
)


@mcp.tool()
def extract_pptx_tool(file_base64: str, filename: str = "upload.pptx") -> str:
    """
    Extract structured content from a PowerPoint (.pptx) file.

    Args:
        file_base64: Base64-encoded content of the .pptx file.
        filename:    Original filename (used for reference in the response).

    Returns:
        JSON string with slide_count and per-slide title, text_blocks, and tables.
    """
    if not filename.lower().endswith((".pptx", ".ppt")):
        raise ValueError("Only .pptx / .ppt files are supported.")

    try:
        data = base64.b64decode(file_base64)
    except Exception as exc:
        raise ValueError(f"Invalid base64 input: {exc}") from exc

    result = extract_pptx(data, filename)
    return json.dumps(result, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # HTTP transport — devtunnel will expose this port
    mcp.run(transport="streamable-http")
