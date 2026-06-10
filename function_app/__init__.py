import json
import logging
import azure.functions as func
from .extractor import extract_pptx

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.route(route="extract-pptx", methods=["POST"])
def extract_pptx_http(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("extract-pptx triggered")

    file = req.files.get("file")
    if not file:
        return func.HttpResponse(
            json.dumps({"error": "Missing 'file' in multipart form data"}),
            status_code=400,
            mimetype="application/json",
        )

    filename = file.filename or "upload.pptx"
    if not filename.lower().endswith((".pptx", ".ppt")):
        return func.HttpResponse(
            json.dumps({"error": "Only .pptx files are supported"}),
            status_code=415,
            mimetype="application/json",
        )

    try:
        result = extract_pptx(file.stream, filename)
        return func.HttpResponse(
            json.dumps(result, ensure_ascii=False, indent=2),
            status_code=200,
            mimetype="application/json",
        )
    except Exception as exc:
        logging.exception("Extraction failed")
        return func.HttpResponse(
            json.dumps({"error": str(exc)}),
            status_code=500,
            mimetype="application/json",
        )
