import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
from typing import List
from sqlmodel import select
from .db import init_db, get_session
from .models import Category, Account, Transaction, Budget, PlannedItem, Attachment
from .utils import generate_bar_chart, generate_line_chart, generate_pie_chart
from datetime import datetime
import json
import re
import os
from .schemas import (
    CategoryCreate, CategoryResponse,
    AccountCreate, AccountResponse,
    TransactionCreate, TransactionResponse,
    BudgetCreate, BudgetResponse,
    PlannedItemCreate, PlannedItemResponse,
    TransferRequest, TransferResponse,
    AIReportRequest, AIReportResponse, ChartInfo,
    HealthResponse
)

UPLOAD_DIR = Path(__file__).resolve().parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="HomeBuh API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/api/health", response_model=HealthResponse)
def health():
    return {"status": "ok"}


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    dest = UPLOAD_DIR / f"{int(datetime.utcnow().timestamp())}_{file.filename}"
    try:
        with open(dest, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"filename": file.filename, "path": str(dest)}


@app.get("/api/uploads/{name}")
def serve_upload(name: str):
    p = UPLOAD_DIR / name
    if not p.exists():
        raise HTTPException(status_code=404, detail="file not found")
    return FileResponse(p)


@app.post("/api/categories", response_model=CategoryResponse)
def create_category(cat: CategoryCreate):
    c = Category(**cat.dict())
    with get_session() as s:
        s.add(c)
        s.commit()
        s.refresh(c)
    return c


@app.get("/api/categories", response_model=List[CategoryResponse])
def list_categories():
    with get_session() as s:
        cats = s.exec(select(Category)).all()
    return cats


@app.post("/api/accounts", response_model=AccountResponse)
def create_account(acc: AccountCreate):
    a = Account(**acc.dict())
    with get_session() as s:
        s.add(a)
        s.commit()
        s.refresh(a)
    return a


@app.get("/api/accounts", response_model=List[AccountResponse])
def list_accounts():
    with get_session() as s:
        accs = s.exec(select(Account)).all()
    return accs


@app.post("/api/transactions", response_model=TransactionResponse)
def create_transaction(tx: TransactionCreate):
    t = Transaction(**tx.dict())
    with get_session() as s:
        s.add(t)
        s.commit()
        s.refresh(t)
    return t


@app.get("/api/transactions", response_model=List[TransactionResponse])
def list_transactions():
    with get_session() as s:
        txs = s.exec(select(Transaction).order_by(Transaction.timestamp.desc())).all()
    return txs


@app.post("/api/budgets", response_model=BudgetResponse)
def create_budget(b: BudgetCreate):
    budget = Budget(**b.dict())
    with get_session() as s:
        s.add(budget)
        s.commit()
        s.refresh(budget)
    return budget


@app.get("/api/budgets", response_model=List[BudgetResponse])
def list_budgets():
    with get_session() as s:
        bs = s.exec(select(Budget)).all()
    return bs


@app.post("/api/planned", response_model=PlannedItemResponse)
def create_planned(p: PlannedItemCreate):
    item = PlannedItem(**p.dict())
    with get_session() as s:
        s.add(item)
        s.commit()
        s.refresh(item)
    return item


@app.get("/api/planned", response_model=List[PlannedItemResponse])
def list_planned():
    with get_session() as s:
        ps = s.exec(select(PlannedItem)).all()
    return ps


@app.post("/api/report")
def generate_report(query: dict):
    """Generate a simple report. Expected JSON: {"type":"expenses_by_category","year_month":"2025-12"} or {"query":"free text"}
    If OPENAI_API_KEY set, will forward prompt to OpenAI (user must configure key).
    """
    prompt = query.get("query")
    # If openai key present, we can optionally forward. For now return a generated chart from data.
    with get_session() as s:
        txs = s.exec(select(Transaction)).all()
    # simple aggregation by category id
    buckets = {}
    labels = []
    values = []
    for t in txs:
        key = str(t.category_id or "Uncategorized")
        buckets[key] = buckets.get(key, 0) + (t.amount or 0)
    for k, v in buckets.items():
        labels.append(k)
        values.append(v)

    from pathlib import Path
    out = Path(__file__).resolve().parent / "reports"
    out.mkdir(parents=True, exist_ok=True)
    chart_path = out / f"report_{int(datetime.utcnow().timestamp())}.png"
    if labels:
        generate_bar_chart(labels, values, chart_path)
    else:
        # create empty placeholder
        with open(chart_path, "wb") as f:
            f.write(b"")

    text = "AI report placeholder."
    # If OPENAI_API_KEY provided, user can change below to call API
    if os.getenv("OPENAI_API_KEY") and prompt:
        try:
            import requests, json
            # Basic example: call OpenAI completions (user must adapt to API version)
            # This is a fallback example; recommend using server-side OpenAI official SDK.
            api_key = os.getenv("OPENAI_API_KEY")
            resp = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"model":"gpt-4o-mini","messages":[{"role":"user","content": prompt}], "max_tokens":500},
                timeout=15,
            )
            if resp.status_code == 200:
                j = resp.json()
                text = j.get("choices", [{}])[0].get("message", {}).get("content", text)
        except Exception:
            pass

    return {"text": text, "chart": f"/api/uploads_report/{chart_path.name}"}


@app.get("/api/uploads_report/{name}")
def serve_report(name: str):
    p = Path(__file__).resolve().parent / "reports" / name
    if not p.exists():
        raise HTTPException(status_code=404, detail="report not found")
    return FileResponse(p)


def _extract_json_from_text(s: str):
    # Try to extract JSON block from model output (strip markdown code fences)
    # Common patterns: ```json { ... } ``` or { ... }
    # First, remove leading/trailing markdown fences
    fence_match = re.search(r"```(?:json)?\n(.*)\n```", s, flags=re.S)
    if fence_match:
        s = fence_match.group(1)
    # Find first { ... } block
    brace_idx = s.find('{')
    if brace_idx == -1:
        return None
    s = s[brace_idx:]
    # Try incremental parsing to find matching braces
    for end in range(len(s), 0, -1):
        try:
            candidate = s[:end]
            return json.loads(candidate)
        except Exception:
            continue
    return None


@app.post("/api/ai/chat", response_model=AIReportResponse)
def ai_chat(request: AIReportRequest):
    """Interactive AI-driven report generation.
    Expected body: {"prompt": "user text describing required report"}

    The model is instructed to return JSON describing:
    {
      "text": "Narrative text",
      "charts": [
         {"type":"bar"|"line"|"pie", "labels":[...], "values":[...], "title":"..."}
      ]
    }

    If `OPENAI_API_KEY` is present, server will forward a structured prompt to OpenAI.
    Otherwise server will attempt to generate a simple sample report from transactions.
    """
    prompt = request.get("prompt") or request.get("query") or ""
    if not prompt:
        raise HTTPException(status_code=400, detail="prompt required")

    # If no API key, generate fallback sample
    if not os.getenv("OPENAI_API_KEY"):
        # simple aggregation by category
        with get_session() as s:
            txs = s.exec(select(Transaction)).all()
        buckets = {}
        for t in txs:
            key = str(t.category_id or "Uncategorized")
            buckets[key] = buckets.get(key, 0) + (t.amount or 0)
        labels = list(buckets.keys())
        values = [buckets[k] for k in labels]
        outdir = Path(__file__).resolve().parent / "reports"
        outdir.mkdir(parents=True, exist_ok=True)
        chart_path = outdir / f"ai_report_{int(datetime.utcnow().timestamp())}.png"
        if labels:
            generate_bar_chart(labels, values, chart_path)
        else:
            with open(chart_path, "wb") as f:
                f.write(b"")
        return {"text": "Fallback AI disabled — sample aggregation.", "charts": [{"url": f"/api/uploads_report/{chart_path.name}", "title": "Sample aggregation"}]}

    # Build system prompt for OpenAI
    system = (
        "You are an assistant that returns a JSON object describing a financial report. "
        "The JSON MUST contain keys: 'text' (string) and optionally 'charts' (array). "
        "Each chart must be an object with 'type' (bar|line|pie), 'labels' (array of strings), 'values' (array of numbers), 'title' (string). "
        "Return JSON only. Do not include extra commentary. If unsure, return empty charts array."
    )

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt},
    ]

    api_key = os.getenv("OPENAI_API_KEY")
    try:
        import requests
        payload = {
            "model": "gpt-4o-mini",
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": 800,
        }
        resp = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=30,
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=502, detail=f"OpenAI error: {resp.status_code}")
        j = resp.json()
        text_out = j.get("choices", [])[0].get("message", {}).get("content", "")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI call failed: {e}")

    # Try parse JSON from model
    parsed = _extract_json_from_text(text_out)
    if not parsed:
        raise HTTPException(status_code=500, detail="Failed to parse JSON from AI response")

    charts_info = parsed.get("charts", [])
    results = []
    outdir = Path(__file__).resolve().parent / "reports"
    outdir.mkdir(parents=True, exist_ok=True)

    for idx, ch in enumerate(charts_info):
        ctype = ch.get("type")
        labels = ch.get("labels", [])
        values = ch.get("values", [])
        title = ch.get("title", f"chart_{idx}")
        fname = f"ai_chart_{int(datetime.utcnow().timestamp())}_{idx}.png"
        outpath = outdir / fname
        try:
            if ctype == "bar":
                generate_bar_chart(labels, values, outpath)
            elif ctype == "line":
                generate_line_chart(labels, values, outpath)
            elif ctype == "pie":
                generate_pie_chart(labels, values, outpath)
            else:
                # unsupported type -> skip
                continue
            results.append({"title": title, "url": f"/api/uploads_report/{fname}"})
        except Exception:
            continue

    return {"text": parsed.get("text", ""), "charts": results}


@app.post("/api/transfer", response_model=TransferResponse)
def transfer(req: TransferRequest):
    """Transfer amount between accounts. Creates two transactions and updates balances."""
    if req.amount <= 0:
        raise HTTPException(status_code=400, detail="amount must be positive")
    with get_session() as s:
        src = s.get(Account, req.from_account_id)
        dst = s.get(Account, req.to_account_id)
        if not src or not dst:
            raise HTTPException(status_code=404, detail="account not found")
        if src.id == dst.id:
            raise HTTPException(status_code=400, detail="source and destination must differ")
        # basic currency check omitted (assume same currency)
        if src.balance < req.amount:
            raise HTTPException(status_code=400, detail="insufficient funds")

        # adjust balances
        src.balance = src.balance - req.amount
        dst.balance = dst.balance + req.amount

        desc1 = req.description or f"Transfer to account {dst.name}"
        desc2 = req.description or f"Transfer from account {src.name}"

        tx1 = Transaction(amount=-abs(req.amount), currency=req.currency or "USD", account_id=src.id, description=desc1)
        tx2 = Transaction(amount=abs(req.amount), currency=req.currency or "USD", account_id=dst.id, description=desc2)

        s.add(src)
        s.add(dst)
        s.add(tx1)
        s.add(tx2)
        s.commit()
        s.refresh(tx1)
        s.refresh(tx2)

    return {"status": "ok", "from_tx": tx1, "to_tx": tx2}
