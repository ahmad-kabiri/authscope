
from __future__ import annotations
import os, asyncio
import typer
from rich import print
from typing import Optional, List, Dict, Any

from authscope.dsl.loader import load_config
from authscope.loaders.openapi_loader import load_openapi, make_scenarios as make_scenarios_from_openapi
from authscope.loaders.har_loader import load_har, make_scenarios_from_har
from authscope.engine.runner import run as run_engine
from authscope.reporters.report import save_json, save_html

app = typer.Typer(help="AuthScope — Authorization invariants tester (MVP)")

@app.command()
def run(
    base: str = typer.Option(..., help="Base URL, e.g., http://127.0.0.1:8000"),
    openapi: str = typer.Option(..., help="Path to OpenAPI YAML"),
    config: str = typer.Option(..., help="Path to config.yaml (subjects & invariants)"),
    out: str = typer.Option("out", help="Output directory"),
    only_get: bool = typer.Option(True, help="Limit to GET operations"),
    har: Optional[str] = typer.Option(None, help="Optional HAR file to enrich scenarios"),
):
    cfg = load_config(config)

    endpoints = load_openapi(openapi, only_get=only_get)
    scenarios = make_scenarios_from_openapi(endpoints)

    if har:
        har_eps = load_har(har, only_get=only_get)
        scenarios += make_scenarios_from_har(har_eps)

    # de-duplicate scenarios by (method,path,tuple(sorted(path_params.items())))
    seen = set()
    uniq = []
    for sc in scenarios:
        key = (sc.method, sc.path, tuple(sorted(sc.path_params.items())))
        if key not in seen:
            seen.add(key)
            uniq.append(sc)
    scenarios = uniq

    print(f"[bold green]Loaded[/] {len(cfg.subjects)} subjects, {len(cfg.invariants)} invariants, {len(scenarios)} scenarios")
    findings = asyncio.run(run_engine(base, cfg.subjects, scenarios, cfg.invariants))
    print(f"[bold yellow]Findings:[/] {len(findings)}")
    save_json(findings, out)
    save_html(findings, out)
    print(f"Saved report to: {os.path.join(out, 'report.html')}")

def main():
    app()

if __name__ == "__main__":
    main()
