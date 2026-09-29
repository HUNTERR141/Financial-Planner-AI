import unittest
from unittest.mock import patch, MagicMock

from app.services.analytics_service import generate_analytics_report
from app.services.forecasting_service import generate_forecast
from app.services.transaction_service import log_transaction
from app.db.models import DBTransaction
from app.context import user_context, get_current_user_id


class TestServices(unittest.TestCase):
    
    @patch('app.services.analytics_service.SessionLocal')
    def test_generate_analytics_report(self, mock_session_local):
        # Mock DB session
        mock_db = MagicMock()
        mock_session_local.return_value = mock_db
        
        # Mock Transactions
        t1 = DBTransaction(id=1, amount=100.0, category='Food', description='Pizza', date='2026-04-01T12:00:00')
        t2 = DBTransaction(id=2, amount=50.0, category='Transport', description='Bus', date='2026-04-02T12:00:00')
        mock_db.query.return_value.filter.return_value.all.return_value = [t1, t2]
        
        with user_context("test-user"):
            report = generate_analytics_report()
        
        self.assertEqual(report.total_spend, 150.0)
        categories = sorted([c.category for c in report.category_breakdown])
        self.assertEqual(categories, ['Food', 'Transport'])
        
    @patch('app.services.transaction_service.create_transaction')
    @patch('app.services.transaction_service.SessionLocal')
    def test_log_transaction_default_local_user(self, mock_session_local, mock_create_transaction):
        mock_db = MagicMock()
        mock_session_local.return_value = mock_db

        mock_db_tx = DBTransaction(
            id=99,
            user_id="local-user",
            amount=120.5,
            description="Groceries",
            category="Food",
            date="2026-09-20T12:00:00"
        )
        mock_create_transaction.return_value = mock_db_tx

        with user_context(None):
            self.assertEqual(get_current_user_id(), "local-user")
            tx = log_transaction(amount=120.5, description="Groceries", category="Food")
            self.assertEqual(tx.amount, 120.5)
            self.assertEqual(tx.id, 99)
            self.assertEqual(tx.category, "Food")

    @patch('app.services.forecasting_service.SessionLocal')
    def test_generate_forecast_no_data(self, mock_session_local):
        # Mock DB session returning no transactions
        mock_db = MagicMock()
        mock_session_local.return_value = mock_db
        mock_db.query.return_value.filter.return_value.all.return_value = []
        
        with user_context("test-user"):
            forecast = generate_forecast()
        self.assertEqual(forecast['predicted_next_month_spend'], 0.0)
        self.assertEqual(forecast['model_used'], 'none')

    @patch('app.services.forecasting_service.SessionLocal')
    def test_generate_forecast_with_data(self, mock_session_local):
        # Mock DB session
        mock_db = MagicMock()
        mock_session_local.return_value = mock_db
        
        t1 = DBTransaction(id=1, amount=100.0, category='Food', description='Pizza', date='2026-04-01T12:00:00')
        t2 = DBTransaction(id=2, amount=100.0, category='Food', description='Burger', date='2026-04-02T12:00:00')
        mock_db.query.return_value.filter.return_value.all.return_value = [t1, t2]
        
        with user_context("test-user"):
            forecast = generate_forecast()
        
        # 2 unique days mapped -> $100 average per day -> * 30 days = $3000
        self.assertAlmostEqual(forecast['predicted_next_month_spend'], 3000.0)
        self.assertEqual(forecast['model_used'], 'daily_average_scaled')
        self.assertIn('Food', forecast['predicted_category_breakdown'])

if __name__ == '__main__':
    unittest.main()
