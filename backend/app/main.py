"""ParseLab API — a thin HTTP boundary over the compiler engine."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import Body, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .core.grammar import analyze_grammar, left_factor
from .core.lexer import analyze_lexer
from .core.ll1 import analyze_ll1
from .core.regex_engine import analyze_regex
from .core.slr import analyze_slr
from .core.timemachine import run_time_machine
from .examples import get_example, list_examples

app = FastAPI(
    title="ParseLab Engine",
    version="1.0.0",
    description="Compiler front-end algorithms: regex, automata, grammars, LL(1), SLR and execution traces.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:4173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ENGINE_MODULES = [
    "regex",
    "thompson-nfa",
    "subset-construction",
    "lexer",
    "grammar",
    "first-follow",
    "ll1",
    "lr0",
    "slr",
    "parse-tree",
    "time-machine",
]


@app.get("/api/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "name": "ParseLab Engine",
        "version": "1.0.0",
        "modules": ENGINE_MODULES,
    }


@app.get("/api/examples")
def examples() -> dict[str, Any]:
    items = list_examples()
    return {
        "examples": items,
        "count": len(items),
        "kinds": sorted({e["kind"] for e in items}),
    }


@app.get("/api/examples/{example_id}")
def example(example_id: str) -> dict[str, Any]:
    item = get_example(example_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Unknown experiment '{example_id}'.")
    return item


@app.post("/api/regex/analyze")
def regex_analyze(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    pattern = payload.get("pattern")
    if not isinstance(pattern, str):
        raise HTTPException(status_code=422, detail="Field 'pattern' must be a string.")
    return analyze_regex(pattern)


@app.post("/api/lexer/analyze")
def lexer_analyze(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    source = payload.get("source", "")
    rules = payload.get("rules", [])
    if not isinstance(source, str):
        raise HTTPException(status_code=422, detail="Field 'source' must be a string.")
    if not isinstance(rules, list):
        raise HTTPException(status_code=422, detail="Field 'rules' must be a list.")
    return analyze_lexer(source, rules)


@app.post("/api/grammar/analyze")
def grammar_analyze(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    text = payload.get("grammar")
    if not isinstance(text, str):
        raise HTTPException(status_code=422, detail="Field 'grammar' must be a string.")
    return analyze_grammar(text)


@app.post("/api/grammar/factor")
def grammar_factor(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    text = payload.get("grammar")
    if not isinstance(text, str):
        raise HTTPException(status_code=422, detail="Field 'grammar' must be a string.")
    return left_factor(text)


@app.post("/api/ll1/analyze")
def ll1_analyze(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    text = payload.get("grammar")
    if not isinstance(text, str):
        raise HTTPException(status_code=422, detail="Field 'grammar' must be a string.")
    input_text = payload.get("input", "")
    if not isinstance(input_text, str):
        raise HTTPException(status_code=422, detail="Field 'input' must be a string.")
    return analyze_ll1(text, input_text)


@app.post("/api/slr/analyze")
def slr_analyze(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    text = payload.get("grammar")
    if not isinstance(text, str):
        raise HTTPException(status_code=422, detail="Field 'grammar' must be a string.")
    input_text = payload.get("input", "")
    if not isinstance(input_text, str):
        raise HTTPException(status_code=422, detail="Field 'input' must be a string.")
    return analyze_slr(text, input_text)


@app.post("/api/timemachine")
def timemachine(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    grammar = payload.get("grammar")
    if not isinstance(grammar, str):
        raise HTTPException(status_code=422, detail="Field 'grammar' must be a string.")
    return run_time_machine(payload)


# ---------------------------------------------------------------------------
# Optional production serving: build the frontend, then run this API.
# ---------------------------------------------------------------------------

_DIST = Path(__file__).resolve().parents[2] / "frontend" / "dist"
if _DIST.exists():
    assets = _DIST / "assets"
    if assets.exists():
        app.mount("/assets", StaticFiles(directory=assets), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    def spa(full_path: str) -> FileResponse:
        if full_path.startswith("api"):
            raise HTTPException(status_code=404, detail="Unknown API route.")
        candidate = _DIST / full_path
        if full_path and candidate.is_file():
            return FileResponse(candidate)
        return FileResponse(_DIST / "index.html")
