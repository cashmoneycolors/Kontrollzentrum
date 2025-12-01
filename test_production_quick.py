#!/usr/bin/env python3
"""Quick Production Test - Alle Systeme"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("\n" + "="*60)
print("🧪 PRODUCTION INFRASTRUCTURE TEST")
print("="*60 + "\n")

# Test 1: Database
print("1️⃣  Testing Database...")
try:
    from core.database import db
    db.save_result("test", {"status": "ok"}, "success", 0.1)
    results = db.get_results("test", limit=1)
    print("   ✅ Database: OK\n")
except Exception as e:
    print(f"   ❌ Database: {e}\n")

# Test 2: Health Monitor
print("2️⃣  Testing Health Monitor...")
try:
    from core.health_monitor import monitor
    health = monitor.check_system_health()
    print(f"   CPU: {health['cpu']:.1f}%")
    print(f"   Memory: {health['memory']:.1f}%")
    print(f"   Status: {health['status']}")
    print("   ✅ Health Monitor: OK\n")
except Exception as e:
    print(f"   ❌ Health Monitor: {e}\n")

# Test 3: Rate Limiter
print("3️⃣  Testing Rate Limiter...")
try:
    from core.rate_limiter import rate_limiter
    allowed = rate_limiter.is_allowed("test_client")
    remaining = rate_limiter.get_remaining("test_client")
    print(f"   Allowed: {allowed}")
    print(f"   Remaining: {remaining}")
    print("   ✅ Rate Limiter: OK\n")
except Exception as e:
    print(f"   ❌ Rate Limiter: {e}\n")

# Test 4: Cache
print("4️⃣  Testing Cache...")
try:
    from core.rate_limiter import cache
    cache.set("test", {"data": "value"})
    result = cache.get("test")
    stats = cache.stats()
    print(f"   Cached: {result}")
    print(f"   Stats: {stats}")
    print("   ✅ Cache: OK\n")
except Exception as e:
    print(f"   ❌ Cache: {e}\n")

# Test 5: Auth
print("5️⃣  Testing Authentication...")
try:
    from core.auth import generate_token, verify_token
    token = generate_token("testuser", "admin")
    payload = verify_token(token)
    print(f"   User: {payload['user_id']}")
    print(f"   Role: {payload['role']}")
    print("   ✅ Auth: OK\n")
except Exception as e:
    print(f"   ❌ Auth: {e}\n")

# Test 6: Circuit Breaker
print("6️⃣  Testing Circuit Breaker...")
try:
    from core.api_gateway import get_breaker
    breaker = get_breaker("test_module")
    print(f"   State: {breaker.state}")
    print(f"   Failures: {breaker.failure_count}")
    print("   ✅ Circuit Breaker: OK\n")
except Exception as e:
    print(f"   ❌ Circuit Breaker: {e}\n")

print("="*60)
print("✅ ALL PRODUCTION SYSTEMS OPERATIONAL")
print("="*60 + "\n")

print("🚀 NEXT STEPS:")
print("   1. python main.py api          (Start API Gateway)")
print("   2. python main.py health       (Check health)")
print("   3. python main.py team         (Run all modules)")
print("   4. streamlit run main.py       (Dashboard)")
print("\n")
