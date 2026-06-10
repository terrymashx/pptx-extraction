# PPTX Extractor — MCP Server

MCP server that extracts structured content (titles, text blocks, tables) from `.pptx` files.
Runs locally and is exposed to the internet via **Microsoft Dev Tunnel** for use with a **Microsoft Copilot Agent**.

## Architecture

```
Copilot Agent (Copilot Studio)
        │  MCP over HTTP
        ▼
  Dev Tunnel URL  ──►  localhost:8000  ──►  server.py  ──►  extractor.py
```

## Quick start

### 1. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start the MCP server

```bash
python server.py
# Server running on http://localhost:8000/mcp
```

### 3. Expose via Microsoft Dev Tunnel

Install the CLI: https://aka.ms/devtunnel/download

```bash
devtunnel login               # sign in with Microsoft account
devtunnel host -p 8000 --allow-anonymous
```

Copy the tunnel URL — it looks like:
`https://abc123-8000.euw.devtunnels.ms`

Your MCP endpoint will be:
`https://abc123-8000.euw.devtunnels.ms/mcp`

### 4. Register in Microsoft Copilot Studio

1. Open your Copilot agent → **Actions** → **Add an action** → **Model Context Protocol**
2. Paste the MCP endpoint URL: `https://<tunnel-url>/mcp`
3. The agent will discover the `extract_pptx` tool automatically

## Tool reference

### `extract_pptx`

| Parameter | Type | Description |
|-----------|------|-------------|
| `file_base64` | string | Base64-encoded `.pptx` file |
| `filename` | string | Original filename (optional, default: `upload.pptx`) |

**Returns** — JSON string:

```json
{
  "filename": "deck.pptx",
  "slide_count": 2,
  "slides": [
    {
      "slide_number": 1,
      "title": "Welcome",
      "text_blocks": ["Intro text", "Key points"],
      "tables": []
    },
    {
      "slide_number": 2,
      "title": "Data",
      "text_blocks": [],
      "tables": [
        [["Header A", "Header B"], ["Value 1", "Value 2"]]
      ]
    }
  ]
}
```

## Test locally (without Copilot)

```python
import base64, json
from extractor import extract_pptx

with open("my-deck.pptx", "rb") as f:
    data = f.read()

result = extract_pptx(data, "my-deck.pptx")
print(json.dumps(result, indent=2))
```
