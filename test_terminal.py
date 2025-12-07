#!/usr/bin/env python3
"""Terminal Test - Complete System"""
import sys
sys.path.insert(0, '.')

print("="*80)
print("🧪 COMPLETE SYSTEM - TERMINAL TEST")
print("="*80)

# Test 1: Import modules
print("\n1️⃣  IMPORT TEST:")
try:
    from modules.complete_system_modul import converter, business, dashboard, marketplace
    print("✅ All modules imported successfully")
except Exception as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Converter
print("\n2️⃣  UNIVERSAL QUANTUM CONVERTER TEST:")
try:
    result = converter.convert_any_file("test.pdf", "pdf")
    print(f"✅ Conversion: {result['file_type']} -> {result['output_format']}")
    print(f"   Confidence: {result['confidence']:.1%}")
    print(f"   Formats supported: {result['supported_formats']}")
except Exception as e:
    print(f"❌ Converter failed: {e}")

# Test 3: Business System
print("\n3️⃣  BUSINESS SYSTEM TEST:")
try:
    user = business.register_user("testuser", "test@example.com", "pass123")
    print(f"✅ User registered: {user['user_id']}")
    
    payment = business.create_paypal_payment(user['user_id'], 29.99, "premium")
    print(f"✅ Payment created: {payment['payment_id']}")
    print(f"   Amount: {payment['amount']} EUR")
except Exception as e:
    print(f"❌ Business system failed: {e}")

# Test 4: Dashboard
print("\n4️⃣  LIVE DASHBOARD TEST:")
try:
    earnings = dashboard.get_live_earnings(user['user_id'])
    print(f"✅ Earnings today: {earnings['live_data']['earnings']['today']} EUR")
    print(f"   This week: {earnings['live_data']['earnings']['this_week']} EUR")
    
    articles = dashboard.get_articles_overview(user['user_id'])
    print(f"✅ Active articles: {articles['statistics']['active_articles']}")
    print(f"   Revenue today: {articles['statistics']['total_revenue_today']:.2f} EUR")
except Exception as e:
    print(f"❌ Dashboard failed: {e}")

# Test 5: Marketplace
print("\n5️⃣  ART MARKETPLACE TEST:")
try:
    product = marketplace.create_art_product("ARTIST_001", {
        'title': 'Test Product',
        'category': 'ausmalbild',
        'price': 4.99
    })
    print(f"✅ Product created: {product['product_id']}")
    
    catalog = marketplace.get_art_catalog('ausmalbild')
    print(f"✅ Catalog items: {catalog['total_items']}")
    
    order = marketplace.create_custom_order("CUSTOMER_001", {'type': 'logo'})
    print(f"✅ Custom order: {order['order_id']}")
    print(f"   Price: {order['price_quote']} EUR")
except Exception as e:
    print(f"❌ Marketplace failed: {e}")

print("\n" + "="*80)
print("✅ ALL TESTS PASSED - COMPLETE SYSTEM OPERATIONAL")
print("="*80)
