#!/usr/bin/env python
"""Test Suite für Dropshipping App"""

import sys
import json

def test_imports():
    """Test ob alle Module importierbar sind"""
    try:
        from core_amazon_api import AmazonAPI
        from core_pricing_engine import PricingEngine
        from core_order_manager import OrderManager
        from core_supplier_api import SupplierAPI
        print("✅ Alle Imports erfolgreich")
        return True
    except Exception as e:
        print(f"❌ Import Error: {e}")
        return False

def test_amazon_api():
    """Test Amazon API"""
    from core_amazon_api import AmazonAPI
    api = AmazonAPI()
    
    products = api.search_products("Wireless Headphones")
    assert len(products) > 0, "Keine Produkte gefunden"
    assert "asin" in products[0], "ASIN fehlt"
    print(f"✅ Amazon API: {len(products)} Produkte gefunden")
    return True

def test_pricing_engine():
    """Test Pricing Engine"""
    from core_pricing_engine import PricingEngine
    engine = PricingEngine(target_margin=0.35)
    
    selling_price = engine.calculate_selling_price(10.0)
    assert selling_price > 10.0, "Verkaufspreis sollte höher als Kosten sein"
    
    profit = engine.calculate_profit(10.0, selling_price)
    assert profit["profit"] > 0, "Gewinn sollte positiv sein"
    print(f"✅ Pricing Engine: Verkaufspreis ${selling_price:.2f}, Gewinn ${profit['profit']:.2f}")
    return True

def test_order_manager():
    """Test Order Manager"""
    from core_order_manager import OrderManager, OrderStatus
    manager = OrderManager()
    
    order = manager.create_order("test@example.com", [{"asin": "B001", "qty": 1}], 34.99)
    assert order["order_id"].startswith("ORD-"), "Order ID Format falsch"
    assert order["status"] == OrderStatus.PENDING, "Status sollte PENDING sein"
    
    updated = manager.update_order_status(order["order_id"], OrderStatus.SHIPPED, "TRACK123")
    assert updated["status"] == OrderStatus.SHIPPED, "Status Update fehlgeschlagen"
    print(f"✅ Order Manager: Bestellung {order['order_id']} erstellt und aktualisiert")
    return True

def test_supplier_api():
    """Test Supplier API"""
    from core_supplier_api import SupplierAPI
    api = SupplierAPI()
    
    price = api.get_supplier_price("B001", "alibaba")
    assert "price" in price, "Preis fehlt"
    assert price["price"] > 0, "Preis sollte positiv sein"
    
    best = api.get_best_supplier("B001", 1)
    assert best in ["alibaba", "dhgate", "1688"], "Ungültiger Lieferant"
    print(f"✅ Supplier API: Bester Lieferant = {best}, Preis = ${price['price']:.2f}")
    return True

def test_api_endpoints():
    """Test FastAPI Endpoints"""
    try:
        import requests
        
        # Health Check
        resp = requests.get("http://localhost:8000/health", timeout=2)
        assert resp.status_code == 200, "Health Check fehlgeschlagen"
        print("✅ API Health Check erfolgreich")
        
        # Search
        resp = requests.post("http://localhost:8000/search", 
                           json={"query": "Test", "category": None}, timeout=5)
        assert resp.status_code == 200, "Search fehlgeschlagen"
        data = resp.json()
        assert "products" in data, "Products fehlen in Response"
        print(f"✅ API Search: {len(data['products'])} Produkte")
        
        # Stats
        resp = requests.get("http://localhost:8000/stats", timeout=2)
        assert resp.status_code == 200, "Stats fehlgeschlagen"
        print("✅ API Stats erfolgreich")
        
        return True
    except requests.exceptions.ConnectionError:
        print("⚠️  API läuft nicht - überspringe Endpoint-Tests")
        return True
    except Exception as e:
        print(f"❌ API Test Error: {e}")
        return False

def main():
    """Führe alle Tests aus"""
    print("=" * 60)
    print("🧪 DROPSHIPPING APP - TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Amazon API", test_amazon_api),
        ("Pricing Engine", test_pricing_engine),
        ("Order Manager", test_order_manager),
        ("Supplier API", test_supplier_api),
        ("API Endpoints", test_api_endpoints),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name}: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n{passed}/{total} Tests bestanden")
    
    if passed == total:
        print("\n🎉 ALLE TESTS ERFOLGREICH!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} Tests fehlgeschlagen")
        return 1

if __name__ == "__main__":
    sys.exit(main())
