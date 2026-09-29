from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.agent_tool import AgentTool

# Sub-agents
from app.agents.transaction_agent import transaction_agent
from app.agents.categorization_agent import categorization_agent
from app.agents.analytics_agent import analytics_agent
from app.agents.forecasting_agent import forecasting_agent
from app.agents.advisor_agent import advisor_agent
from app.agents.memory_agent import memory_agent

def orchestrator() -> LlmAgent:
    instructions = """You are the Orchestrator agent for the Financial Planner AI system.

Your role is to route user intents to the appropriate specialized financial agents. 
You are the central point of contact for the user. 

Available agents:
1. **transaction_agent**: Handles natural-language transaction logging.
2. **categorization_agent**: Categorizes transactions into relevant categories (e.g., groceries, rent).
3. **analytics_agent**: Analyzes spending habits, computes trends, and provides statistical summaries.
4. **forecasting_agent**: Forecasts future expenses, cash flows, and budgets based on trends.
5. **advisor_agent**: Gives general financial advice, saving tips, and suggestions.
6. **memory_agent**: Manages long term user memory and retrieves historical context.

Routing rules:
- intent 'transaction' -> Route to transaction_agent
- intent 'categorize' -> Route to categorization_agent
- intent 'analytics' -> Route to analytics_agent
- intent 'forecast' -> Route to forecasting_agent
- intent 'advice' -> Route to advisor_agent

When to trigger the memory_agent:
- Whenever there is enough historical data that needs to be aggregated and stored.
- When the user asks for historical insights that span across many months or sessions.
- Always check memory context before providing deeply personalized advice.

Instructions:
1. Interpret the user intent clearly.
2. Check if a memory retrieval is needed first.
3. Call the accurate agent to fulfill the request.
4. Return the exact response from the agent to the user without summarizing it.
"""

    return LlmAgent(
        name="orchestrator",
        model="gemini-3.6-flash",
        instruction=instructions,
        tools=[
            AgentTool(transaction_agent()),
            AgentTool(categorization_agent()),
            AgentTool(analytics_agent()),
            AgentTool(forecasting_agent()),
            AgentTool(advisor_agent()),
            AgentTool(memory_agent()),
        ]
    )
