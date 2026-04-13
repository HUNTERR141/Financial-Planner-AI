# 💰 Financial Planner AI

> A multi-agent AI-powered personal finance assistant built with **Google ADK** and **FastAPI** — tracks your spending, categorizes transactions, forecasts future expenses, and gives personalized financial advice.

---

## 🚀 Features

- 🔀 **Orchestrator Agent** — Routes user intent to the right specialized agent automatically
- 💳 **Transaction Agent** — Log, retrieve, and delete financial transactions
- 🏷️ **Categorization Agent** — Auto-categorizes transactions (groceries, rent, entertainment, etc.)
- 📊 **Analytics Agent** — Spending trends, category breakdowns, and statistical summaries
- 📈 **Forecasting Agent** — Predicts future expenses and cash flow based on historical trends
- 🧠 **Memory Agent** — Stores long-term user insights across sessions for personalized context
- 💡 **Advisor Agent** — Delivers empathetic, data-driven financial advice with actionable tips

---

## 🏗️ Project Structure

```
FinancialPlanner/
├── app/
│   ├── agents/                  # Specialized AI agents
│   │   ├── advisor_agent.py
│   │   ├── analytics_agent.py
│   │   ├── categorization_agent.py
│   │   ├── forecasting_agent.py
│   │   ├── memory_agent.py
│   │   └── transaction_agent.py
│   ├── api/                     # FastAPI routes & dependencies
│   │   └── routes/
│   ├── config/                  # Pydantic settings & environment config
│   ├── db/                      # SQLAlchemy models & database setup
│   ├── memory/                  # Context manager for long-term memory
│   ├── prompts/                 # Agent prompt templates (.txt)
│   ├── schemas/                 # Pydantic request/response schemas
│   ├── services/                # Business logic layer
│   ├── tools/                   # Agent tools (db, analytics, forecasting, memory)
│   ├── orchestrator.py          # Root orchestrator agent
│   └── main.py                  # ADK app entrypoint
├── data/                        # Sample data files (JSON)
├── tests/                       # Test suite
├── adk.yaml                     # ADK agent & tool registry
├── requirements.txt
└── .env                         # Environment variables (not committed)
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| AI / Agents | [Google ADK](https://google.github.io/adk-docs/) + Gemini 2.5 Flash |
| API Framework | FastAPI + Uvicorn |
| Database | SQLite via SQLAlchemy 2.0 |
| Validation | Pydantic v2 + pydantic-settings |
| Language | Python 3.11+ |

---

## 🛠️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/HUNTERR141/FinancialPlanner.git
cd FinancialPlanner
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key_here
DATABASE_URL=sqlite:///./financial_data.db
```

> **Note:** Never commit your `.env` file. It is already listed in `.gitignore`.

---

## ▶️ Running the App

### Using FastAPI directly

```bash
uvicorn app.main:app --reload
```

API docs available at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## 🤖 Agent Architecture

```
User Input
    │
    ▼
┌─────────────────┐
│   Orchestrator  │  ← Routes intent to the right agent
└────────┬────────┘
         │
   ┌─────┴──────────────────────────────────┐
   │         │          │         │         │
   ▼         ▼          ▼         ▼         ▼
Transaction  Categ.  Analytics  Forecast  Advisor
  Agent      Agent    Agent      Agent     Agent
                                            │
                                            ▼
                                       Memory Agent
                                    (cross-session context)
```

---

## 📦 Environment Variables

| Variable | Description | Required |
|---|---|---|
| `GOOGLE_API_KEY` | Google Gemini API key for ADK agents | ✅ |
| `DATABASE_URL` | SQLAlchemy database connection string | ✅ |

---

## 🔮 Future Improvements

- UPI and SMS transaction parser
- Dashboard(good frontend)
- Security and threat detection

## Contributing

  Contributions are welcome.
- Fork the repo
- Create a new branch(branch\your_feature)
- Commit changes
- Push the changes and generate PR


## 🙌 Acknowledgements

- [Google ADK](https://google.github.io/adk-docs/) — Agent Development Kit
- [FastAPI](https://fastapi.tiangolo.com/) — Modern Python web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) — Python SQL toolkit


## ⭐Show your support

 Give a star⭐ if you liked my project. <br>
 Thank you.