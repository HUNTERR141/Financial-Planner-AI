import os

# Root Paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

# Core Paths
DEFAULT_DB_PATH = os.path.join(PROJECT_ROOT, "financial_data.db")
CATEGORIES_FILE_PATH = os.path.join(DATA_DIR, "categories.json")

# Application Constants
DEFAULT_CURRENCY = "USD"
MAX_TRANSACTION_LIMIT_PER_QUERY = 1000

# Agent Names mapping
ORCHESTRATOR_AGENT = "orchestrator"
TRANSACTION_AGENT = "transaction_agent"
CATEGORIZATION_AGENT = "categorization_agent"
ANALYTICS_AGENT = "analytics_agent"
FORECASTING_AGENT = "forecasting_agent"
ADVISOR_AGENT = "advisor_agent"
MEMORY_AGENT = "memory_agent"
