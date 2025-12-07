Backend (FastAPI)

Run locally:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Environment:
- `OPENAI_API_KEY` (optional) — если хотите, чтобы AI-отчёты использовали OpenAI
