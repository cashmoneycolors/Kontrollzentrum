"""
Unit Tests - Alle Module
"""
import unittest
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

class TestModules(unittest.TestCase):
    def test_beispiel_modul(self):
        """Test: Beispiel-Modul"""
        try:
            from modules.beispiel_modul import run
            result = run()
            self.assertIsNotNone(result)
            self.assertEqual(result.get("status"), "ok")
        except Exception as e:
            self.fail(f"Beispiel-Modul fehlgeschlagen: {e}")
    
    def test_key_check(self):
        """Test: Key-Prüfung"""
        try:
            from core.key_check import REQUIRED_KEYS
            self.assertGreater(len(REQUIRED_KEYS), 0)
        except Exception as e:
            self.fail(f"Key-Check fehlgeschlagen: {e}")
    
    def test_api_gateway(self):
        """Test: API Gateway"""
        try:
            from core.api_gateway import app
            self.assertIsNotNone(app)
        except Exception as e:
            self.fail(f"API Gateway fehlgeschlagen: {e}")
    
    def test_health_monitor(self):
        """Test: Health Monitor"""
        try:
            from core.health_monitor import monitor
            health = monitor.check_system_health()
            self.assertIn("cpu", health)
            self.assertIn("memory", health)
        except Exception as e:
            self.fail(f"Health Monitor fehlgeschlagen: {e}")

if __name__ == "__main__":
    unittest.main()
