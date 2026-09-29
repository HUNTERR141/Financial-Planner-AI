# Usage Guide

This project runs in a local Python environment and exposes a FastAPI application plus the AI agent system. Use the commands below from the project root in PowerShell or Command Prompt.

---

## 1. Open terminal in the project folder

```bash
cd "D:\work\Projects\FinancialPLanner"
```

If you are in a different folder:

```bash
cd path\to\FinancialPlanner
```

---

## 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

Verify activation:

```bash
python --version
pip --version
```

---

## 3. Upgrade pip (optional but recommended)

```bash
python -m pip install --upgrade pip
```

---

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

If you see missing package errors later, run this again after activation:

```bash
pip install -r requirements.txt
```

---

## 5. Create environment file

Create a file named `.env` in the project root with:

```env
GOOGLE_API_KEY=your_google_api_key_here
DATABASE_URL=sqlite:///./financial_data.db
CORS_ORIGINS=http://localhost:3000
```

Example for local testing:

```env
GOOGLE_API_KEY=AIza...your_key_here
DATABASE_URL=sqlite:///./financial_data.db
CORS_ORIGINS=http://localhost:3000
```

Important:
- Do not commit `.env` to source control.
- This app is intended for a single local user, so no API key or user ID header is required during normal use.

---

## 6. Run the app

From the project root:

```bash
uvicorn app.api.main:app --reload --host 127.0.0.1 --port 8000
```

Then open:

- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

To stop the server, press:

```bash
Ctrl + C
```

---

## 7. Run tests

```bash
python -m unittest discover -s tests -v
```

This project uses the default unittest runner.

If you get import errors, make sure the virtual environment is active and dependencies were installed:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

---

## 8. Example API requests

This local version is designed for one user, so requests do not need `X-API-Key` or `X-User-ID` headers.

### Health check

```bash
curl http://localhost:8000/health
```

### Add a transaction through the agent

```bash
curl -X POST "http://localhost:8000/api/v1/transactions/" ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"I spent $45 on groceries at Walmart yesterday\"}"
```

### Get transaction history

```bash
curl "http://localhost:8000/api/v1/transactions/?skip=0&limit=20"
```

### Ask for AI financial insights

```bash
curl "http://localhost:8000/api/v1/insights/?query=Where%20did%20I%20spend%20most%3F"
```

### Get raw analytics data

```bash
curl "http://localhost:8000/api/v1/insights/raw"
```

### Get raw forecast

```bash
curl "http://localhost:8000/api/v1/insights/forecast/raw"
```

### Chat with the advisor

```bash
curl -X POST "http://localhost:8000/api/v1/user/chat" ^
  -H "Content-Type: application/json" ^
  -d "{\"query\":\"Give me a simple budget plan for the next month\"}"
```

---

## 9. Common troubleshooting

### Missing module errors like `No module named 'sqlalchemy'`

```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

### API returns 500

Check:
- `GOOGLE_API_KEY` is set correctly
- the Google ADK dependencies are installed
- the server is running from a valid project environment

---

## 10. Typical full workflow

```bash
cd "D:\work\Projects\FinancialPLanner"
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy NUL .env
```

Then open `.env` and add your values, then start the app:

```bash
uvicorn app.api.main:app --reload --host 127.0.0.1 --port 8000
```

In a second terminal, test:

```bash
curl http://localhost:8000/health
```

You can now send natural-language expense messages like:

```bash
curl -X POST "http://localhost:8000/api/v1/transactions/" ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"I spent $120 on groceries today\"}"
```

This will save the transaction under the local single-user profile automatically.

---

## 11. Quick start summary

```bash
cd "D:\work\Projects\FinancialPLanner"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` with the required values, then:

```bash
uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000
```

Use the API docs at:

```text
http://localhost:8000/docs
```
