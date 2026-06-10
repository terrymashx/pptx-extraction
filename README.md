# PPTX Extractor — Azure Function App

HTTP-triggered Azure Function that extracts structured content (titles, text, tables) from `.pptx` files. Designed to be registered as a plugin action in a **Microsoft Copilot Agent**.

## Endpoint

```
POST /api/extract-pptx
Content-Type: multipart/form-data
x-functions-key: <your-key>

file: <binary .pptx>
```

### Response example

```json
{
  "filename": "deck.pptx",
  "slide_count": 3,
  "slides": [
    {
      "slide_number": 1,
      "title": "Welcome",
      "text_blocks": ["This is the intro slide", "Key points here"],
      "tables": []
    },
    {
      "slide_number": 2,
      "title": "Data",
      "text_blocks": [],
      "tables": [
        [["Header A", "Header B"], ["Row 1A", "Row 1B"]]
      ]
    }
  ]
}
```

## Local development

```bash
cd pptx-extractor
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt azure-functions-core-tools
func start
```

Test with curl:
```bash
curl -X POST http://localhost:7071/api/extract-pptx \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your-deck.pptx"
```

## Deploy to Azure

### 1. Create infrastructure (once)

```bash
az group create --name rg-pptx-extractor --location westeurope

az storage account create \
  --name stpptxextractor \
  --resource-group rg-pptx-extractor \
  --sku Standard_LRS

az functionapp create \
  --name <YOUR_APP_NAME> \
  --resource-group rg-pptx-extractor \
  --storage-account stpptxextractor \
  --consumption-plan-location westeurope \
  --runtime python \
  --runtime-version 3.11 \
  --functions-version 4 \
  --os-type linux
```

### 2. Add GitHub secrets

| Secret | Value |
|--------|-------|
| `AZURE_FUNCTIONAPP_NAME` | Your function app name |
| `AZURE_FUNCTIONAPP_PUBLISH_PROFILE` | Download from Azure Portal → Function App → Get publish profile |

Push to `main` to trigger deployment automatically.

## Register in Microsoft Copilot Studio

1. Open your Copilot agent in **Copilot Studio**
2. Go to **Actions** → **Add an action** → **New action from OpenAPI**
3. Upload [`openapi.json`](./openapi.json) (update the `servers.url` with your function app URL first)
4. Add an **API key** connection using the Function App host key
5. The agent can now call `extractPptx` as a tool action
