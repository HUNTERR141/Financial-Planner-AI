from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.db.session import init_db
from app.api.routes import transactions, insights, user

def create_app() -> FastAPI:
    # Safely boot up the SQLite tables synchronously before HTTP begins
    init_db()

    app = FastAPI(
        title=settings.APP_NAME,
        description="Production API securely integrating custom financial tools with modern Agent-driven AI workflows.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Permissive cross-origin config; modify before launching to true prod domain mapping
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Attach isolated domains securely
    app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["Transactions"])
    app.include_router(insights.router,     prefix="/api/v1/insights",     tags=["Insights Data & Analytics"])
    app.include_router(user.router,         prefix="/api/v1/user",         tags=["User Chat & Advising"])

    @app.get("/health", tags=["Health Checks"])
    async def health_check():
        return {
            "status": "online",
            "app_name": settings.APP_NAME,
            "agent_cluster": "active"
        }

    return app

# The instantiated application entry point
app = create_app()
