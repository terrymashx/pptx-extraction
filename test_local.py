"""
Quick local test — no server needed.
Creates a tiny in-memory .pptx and runs the extractor.
"""
import json
import base64
import io

from pptx import Presentation
from pptx.util import Inches
from extractor import extract_pptx


def make_sample_pptx() -> bytes:
    """Build a small 2-slide deck in memory."""
    prs = Presentation()
    layout = prs.slide_layouts[1]  # Title + Content

    # Slide 1 — text
    s1 = prs.slides.add_slide(layout)
    s1.shapes.title.text = "Welcome"
    s1.placeholders[1].text = "This is the intro slide\nWith multiple lines"

    # Slide 2 — table
    s2 = prs.slides.add_slide(prs.slide_layouts[5])  # blank
    s2.shapes.title is None  # blank layout has no title placeholder
    rows, cols = 3, 2
    table = s2.shapes.add_table(rows, cols, Inches(1), Inches(1), Inches(6), Inches(2)).table
    headers = ["Name", "Score"]
    data    = [["Alice", "95"], ["Bob", "87"]]
    for col_idx, h in enumerate(headers):
        table.cell(0, col_idx).text = h
    for row_idx, row in enumerate(data, start=1):
        for col_idx, val in enumerate(row):
            table.cell(row_idx, col_idx).text = val

    buf = io.BytesIO()
    prs.save(buf)
    return buf.getvalue()


def main():
    print("=== Test 1: extractor directly ===")
    pptx_bytes = make_sample_pptx()
    result = extract_pptx(pptx_bytes, "sample.pptx")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    print("\n=== Test 2: via base64 (simulates MCP call) ===")
    b64 = base64.b64encode(pptx_bytes).decode()
    import base64 as b64mod
    decoded = b64mod.b64decode(b64)
    result2 = extract_pptx(decoded, "sample.pptx")
    assert result == result2
    print("Base64 round-trip OK ✓")
    print(f"slide_count: {result2['slide_count']}")
    print(f"Slide 1 title: {result2['slides'][0]['title']}")
    print(f"Slide 2 table: {result2['slides'][1]['tables']}")


if __name__ == "__main__":
    main()
