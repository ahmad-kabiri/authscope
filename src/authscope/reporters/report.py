
from __future__ import annotations
import json, os, html
from typing import List
from authscope.core.models import Finding

def save_json(findings: List[Finding], outdir: str):
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "findings.json"), "w", encoding="utf-8") as f:
        json.dump([f.model_dump() for f in findings], f, indent=2, ensure_ascii=False)

def save_html(findings: List[Finding], outdir: str):
    os.makedirs(outdir, exist_ok=True)
    rows = []
    for f in findings:
        rows.append(
            '<tr>'
            f'<td>{html.escape(f.invariant)}</td>'
            f'<td><code>{html.escape(f.method)} {html.escape(f.path)}</code></td>'
            f'<td>{html.escape(f.subject)}</td>'
            '<td>'
            f'<div>Status: {f.evidence.status}</div>'
            '<details><summary>Headers</summary>'
            f'<pre>{html.escape(str(f.evidence.headers))}</pre></details>'
            '<details><summary>Body</summary>'
            f'<pre>{html.escape(f.evidence.body[:2000])}</pre></details>'
            '</td>'
            '</tr>'
        )
    html_doc = (
        "<html><head>"
        '<meta charset="utf-8"/>'
        "<title>AuthScope Report</title>"
        "<style>"
        "body { font-family: system-ui, sans-serif; margin: 2rem; }"
        "table { border-collapse: collapse; width: 100%; }"
        "th, td { border: 1px solid #ddd; padding: 8px; vertical-align: top; }"
        "th { background: #f5f5f5; }"
        "code { background: #f0f0f0; padding: 0.1rem 0.2rem; border-radius: 4px; }"
        "details > summary { cursor: pointer; }"
        "</style>"
        "</head><body>"
        "<h1>AuthScope Findings</h1>"
        "<table>"
        "<thead><tr><th>Invariant</th><th>Endpoint</th><th>Subject</th><th>Evidence</th></tr></thead>"
        "<tbody>"
        + ("".join(rows) if findings else '<tr><td colspan="4">No findings.</td></tr>')
        + "</tbody></table></body></html>"
    )
    with open(os.path.join(outdir, "report.html"), "w", encoding="utf-8") as f:
        f.write(html_doc)
