# ParseLab

ParseLab is an interactive compiler front-end laboratory. Its Python engine computes lexer results, Thompson NFAs and subset DFAs, grammar diagnostics, FIRST/FOLLOW sets, LL(1) and SLR tables, parser simulations, parse trees, and end-to-end traces. The React interface makes those results inspectable.

## What it does

| Bench | Algorithms |
|---|---|
| Automata studio | Regex parser → Thompson ε-NFA → subset-construction DFA → **minimal DFA** (partition refinement, every round explained); live string test with the path highlighted |
| Lexical analysis | Maximal-munch scanner driven by your regex rules, with rule-priority tie breaking, skip rules, positions and error recovery |
| Grammar workbench | FIRST / FOLLOW / nullable by fixed point, diagnostics (direct, indirect and *hidden* left recursion, unreachable / non-productive symbols, unit cycles), plus one-click **left-recursion elimination** and **left factoring** with step-by-step explanations |
| LL(1) parsing | Predictive table with conflict explanations, step-by-step simulation, parse tree that grows as you step, leftmost/rightmost derivations |
| LR parsing | **SLR(1), LALR(1) and canonical LR(1)** automata and ACTION/GOTO tables (LALR shows which LR(1) states it merged), conflict reports, bottom-up trace and tree, plus a **parser-class strip** that checks the grammar against LL(1) / SLR / LALR / LR(1) at once and explains the verdict |
| Time machine | One synchronised trace from source characters → tokens → parser decisions → tree, in LL(1) or SLR(1) mode, with play/pause |

Every parse tree can be exported as **SVG, PNG or LaTeX** (`qtree`) for reports. The **Share** button copies a link that reopens the exact experiment (grammar, input, method), so it can be sent to classmates or a teacher on the same network.

Keyboard: `Ctrl/⌘ + Enter` runs the bench, `←` / `→` step through a trace, `Space` plays or pauses.

## Run locally

Use Python 3.10 or newer and Node.js 18 or newer.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
uvicorn app.main:app --app-dir backend --reload --host 127.0.0.1 --port 8001
```

In another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal. Vite listens on all network interfaces and proxies `/api` requests to the local backend on port 8001. Set `PARSELAB_API_TARGET` before starting Vite to use a different backend address. FastAPI also serves `frontend/dist` when a production build is present.

## Open ParseLab on another device on the same Wi-Fi

1. Start the API and frontend using the commands above. Keep both terminal windows running.
2. Find this computer's IPv4 address with `ipconfig` (use the address under the active Wi-Fi adapter, usually `192.168.x.x` or `10.x.x.x`).
3. On the phone or other computer, open `http://<that-ip>:5173` — for example, `http://192.168.1.24:5173`.

Both devices must be on the same local network. If Windows Firewall asks, allow Python and Node.js on **Private networks**. Do not choose Public networks for a home or school Wi-Fi connection.

## Tests

```powershell
pip install -r backend
equirements-dev.txt
cd backend
python -m pytest -q
```

## API

Interactive API documentation is available at `http://127.0.0.1:8001/docs`. Health and example endpoints are `GET /api/health` and `GET /api/examples`.
