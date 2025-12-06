"""Unit Tests - Alle Module testen"""
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules import ai_assistant, data_analytics, email_automation, customer_crm

class TestAIAssistant(unittest.TestCase):
    def test_run(self):
        result = ai_assistant.run()
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['confidence'], 1.0)

class TestDataAnalytics(unittest.TestCase):
    def test_run(self):
        result = data_analytics.run()
        self.assertEqual(result['status'], 'success')
        self.assertIn('stats', result)

class TestEmailAutomation(unittest.TestCase):
    def test_run(self):
        result = email_automation.run()
        self.assertEqual(result['status'], 'success')
        self.assertGreater(result['sent'], 0)

class TestCustomerCRM(unittest.TestCase):
    def test_run(self):
        result = customer_crm.run()
        self.assertEqual(result['status'], 'success')
        self.assertGreater(result['analyzed'], 0)

if __name__ == '__main__':
    unittest.main()
