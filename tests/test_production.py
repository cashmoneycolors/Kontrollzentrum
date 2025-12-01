"""Production Infrastructure Tests"""
import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database import db
from core.health_monitor import monitor
from core.rate_limiter import rate_limiter, cache
from core.auth import generate_token, verify_token
import time

class TestDatabase(unittest.TestCase):
    def test_save_and_get_results(self):
        db.save_result("test_module", {"data": "test"}, "success", 0.5)
        results = db.get_results("test_module", limit=1)
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0]["module"], "test_module")
    
    def test_config_storage(self):
        db.set_config("test_key", {"value": 123})
        result = db.get_config("test_key")
        self.assertEqual(result["value"], 123)
    
    def test_audit_log(self):
        db.audit("TEST_ACTION", "testuser", "Test details")
        logs = db.get_audit_log(limit=1)
        self.assertTrue(len(logs) > 0)

class TestHealthMonitor(unittest.TestCase):
    def test_system_health(self):
        health = monitor.check_system_health()
        self.assertIn("cpu", health)
        self.assertIn("memory", health)
        self.assertIn("disk", health)
        self.assertIn("status", health)
    
    def test_health_status_values(self):
        health = monitor.check_system_health()
        self.assertIn(health["status"], ["healthy", "warning", "critical"])

class TestRateLimiter(unittest.TestCase):
    def test_rate_limit_allowed(self):
        self.assertTrue(rate_limiter.is_allowed("client1"))
    
    def test_rate_limit_exceeded(self):
        client = "test_client"
        for _ in range(100):
            rate_limiter.is_allowed(client)
        self.assertFalse(rate_limiter.is_allowed(client))
    
    def test_remaining_requests(self):
        remaining = rate_limiter.get_remaining("new_client")
        self.assertGreater(remaining, 0)

class TestCache(unittest.TestCase):
    def test_cache_set_get(self):
        cache.set("test_module", {"result": "data"})
        result = cache.get("test_module")
        self.assertEqual(result["result"], "data")
    
    def test_cache_expiry(self):
        cache.ttl = 1
        cache.set("expire_test", {"data": "test"})
        time.sleep(1.1)
        result = cache.get("expire_test")
        self.assertIsNone(result)
        cache.ttl = 300
    
    def test_cache_stats(self):
        stats = cache.stats()
        self.assertIn("total_entries", stats)
        self.assertIn("valid_entries", stats)

class TestAuth(unittest.TestCase):
    def test_token_generation(self):
        token = generate_token("testuser", "user")
        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)
    
    def test_token_verification(self):
        token = generate_token("testuser", "admin")
        payload = verify_token(token)
        self.assertEqual(payload["user_id"], "testuser")
        self.assertEqual(payload["role"], "admin")
    
    def test_invalid_token(self):
        with self.assertRaises(Exception):
            verify_token("invalid.token.here")

class TestCircuitBreaker(unittest.TestCase):
    def test_circuit_breaker_state(self):
        from core.api_gateway import get_breaker
        breaker = get_breaker("test_module")
        self.assertEqual(breaker.state, "CLOSED")
    
    def test_circuit_breaker_opens(self):
        from core.api_gateway import get_breaker
        breaker = get_breaker("failing_module")
        breaker.failure_threshold = 2
        
        for _ in range(2):
            try:
                breaker.call(lambda: 1/0)
            except:
                pass
        
        self.assertEqual(breaker.state, "OPEN")

if __name__ == "__main__":
    unittest.main(verbosity=2)
