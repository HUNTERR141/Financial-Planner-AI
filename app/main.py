import os

from app.config.settings import settings

if settings.GOOGLE_API_KEY:
    os.environ.setdefault("GOOGLE_API_KEY", settings.GOOGLE_API_KEY)

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService

from app.orchestrator import orchestrator

def main():
    """
    Initialize the ADK Runner with the orchestrator as the root agent.
    We configure InMemorySessionService and InMemoryMemoryService for shared
    session memory context across all agents.
    """
    root_agent = orchestrator()
    
    runner = Runner(
        agent=root_agent,
        app_name="Financial Planner AI",
        memory_service=InMemoryMemoryService(),
        session_service=InMemorySessionService(),
        auto_create_session=True,
    )
    
    return runner

if __name__ == "__main__":
    runner = main()
    runner.run()
