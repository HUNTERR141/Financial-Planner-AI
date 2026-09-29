import unittest
from unittest.mock import patch, MagicMock

# Import agents
from app.agents.analytics_agent import analytics_agent
from app.agents.forecasting_agent import forecasting_agent
from app.agents.advisor_agent import advisor_agent
from app.agents.memory_agent import memory_agent
from app.agents.categorization_agent import categorization_agent
from app.agents.transaction_agent import transaction_agent
from app.orchestrator import orchestrator


class TestAgents(unittest.TestCase):
    """
    Validates correct properties on instantiated LLM Agents including expected tool assignments and names
    without pinging real un-mocked Google/OpenAI network layers.
    """

    def test_analytics_agent_init(self):
        agent = analytics_agent()
        self.assertEqual(agent.name, "analytics_agent")
        self.assertEqual(len(agent.tools), 1)
        self.assertEqual(agent.tools[0].__name__, "get_spending_analytics")

    def test_forecasting_agent_init(self):
        agent = forecasting_agent()
        self.assertEqual(agent.name, "forecasting_agent")
        self.assertEqual(len(agent.tools), 1)
        self.assertEqual(agent.tools[0].__name__, "get_future_forecast")

    def test_advisor_agent_init(self):
        agent = advisor_agent()
        self.assertEqual(agent.name, "advisor_agent")
        self.assertEqual(len(agent.tools), 3)
        tool_names = [t.__name__ for t in agent.tools]
        self.assertIn("get_full_advisor_context", tool_names)
        self.assertIn("remember_insight", tool_names)

    def test_memory_agent_init(self):
        agent = memory_agent()
        self.assertEqual(agent.name, "memory_agent")
        self.assertEqual(len(agent.tools), 3)
        tool_names = [t.__name__ for t in agent.tools]
        self.assertIn("get_raw_transaction_history", tool_names)
        self.assertIn("save_financial_insight", tool_names)

    def test_orchestrator_init(self):
        agent = orchestrator()
        self.assertEqual(agent.name, "orchestrator")
        self.assertGreaterEqual(len(agent.tools), 6) # At least 6 sub-agents attached
        
    @patch('app.agents.categorization_agent.get_allowed_categories')
    def test_categorization_tools_mock(self, mock_get_allowed):
        """Proof of concept executing tool mocking."""
        mock_get_allowed.return_value = ["Food", "Rent", "Entertainment"]
        agent = categorization_agent()
        self.assertEqual(agent.name, "categorization_agent")

if __name__ == '__main__':
    unittest.main()
