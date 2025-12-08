"""
Rate Limiting & Caching
"""
import time
from functools import wraps
from collections import defaultdict

class RateLimiter:
    def __init__(self, per_minute=100):
        self.per_minute = per_minute
        self.requests = defaultdict(list)
    
    def is_allowed(self, key):
        """Prüft ob Request erlaubt ist"""
        now = time.time()
        minute_ago = now - 60
        
        self.requests[key] = [t for t in self.requests[key] if t > minute_ago]
        
        if len(self.requests[key]) < self.per_minute:
            self.requests[key].append(now)
            return True
        return False

class Cache:
    def __init__(self, ttl=300):
        self.ttl = ttl
        self.cache = {}
    
    def get(self, key):
        """Holt aus Cache"""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            del self.cache[key]
        return None
    
    def set(self, key, value):
        """Speichert in Cache"""
        self.cache[key] = (value, time.time())

rate_limiter = RateLimiter()
cache = Cache()
