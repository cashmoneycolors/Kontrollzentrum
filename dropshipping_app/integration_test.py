#!/usr/bin/env python
"""Integration Test - Simuliert kompletten Workflow"""

def test_complete_workflow():
    """Teste kompletten Dropshipping-Workflow"""
    
    print("\n" + "=" * 60)
    print("🔄 INTEGRATION TEST - KOMPLETTER WORKFLOW")
    print("=" * 60)
    
    # 1. Produktsuche
    print("\n[1/5] Produktsuche...")
    from core_amazon_api import AmazonAPI
    amazon = AmazonAPI()
    products = amazon.search_products("Wireless Headphones")
    assert len(products) > 0
    product = products[0]
    print(f"  ✅ Gefunden: {product['title'][:50]}")
    print(f"     ASIN: {product['asin']}")
    print(f"     Amazon Preis: ${product['price']:.2f}")
    
    # 2. Lieferant finden
    print("\n[2/5] Lieferant finden...")
    from core_supplier_api import SupplierAPI
    supplier_api = SupplierAPI()
    best_supplier = supplier_api.get_best_supplier(product['asin'], 1)
    supplier_price = supplier_api.get_supplier_price(product['asin'], best_supplier)
    print(f"  ✅ Bester Lieferant: {best_supplier}")
    print(f"     Lieferantenpreis: ${supplier_price['price']:.2f}")
    print(f"     Lieferzeit: {supplier_price['lead_time']} Tage")
    
    # 3. Preis berechnen
    print("\n[3/5] Preis berechnen...")
    from core_pricing_engine import PricingEngine
    pricing = PricingEngine(target_margin=0.35)
    selling_price = pricing.calculate_selling_price(supplier_price['price'])
    profit_info = pricing.calculate_profit(supplier_price['price'], selling_price)
    print(f"  ✅ Verkaufspreis: ${selling_price:.2f}")
    print(f"     Gewinn: ${profit_info['profit']:.2f}")
    print(f"     Margin: {profit_info['margin_percent']:.1f}%")
    
    # 4. Bestellung erstellen
    print("\n[4/5] Bestellung erstellen...")
    from core_order_manager import OrderManager
    order_mgr = OrderManager()
    order = order_mgr.create_order(
        "customer@example.com",
        [{"asin": product['asin'], "qty": 1}],
        selling_price
    )
    print(f"  ✅ Bestellung erstellt: {order['order_id']}")
    print(f"     Kunde: {order['customer_email']}")
    print(f"     Betrag: ${order['total']:.2f}")
    print(f"     Status: {order['status']}")
    
    # 5. Fulfillment
    print("\n[5/5] Automatische Fulfillment...")
    supplier_order = supplier_api.place_supplier_order(
        best_supplier,
        [{"asin": product['asin'], "qty": 1}],
        "123 Main St, City, Country"
    )
    tracking = supplier_order['tracking']
    fulfilled = order_mgr.auto_fulfill_order(order['order_id'], tracking)
    print(f"  ✅ Fulfillment abgeschlossen")
    print(f"     Tracking: {tracking}")
    print(f"     Status: {fulfilled['status']}")
    
    # Zusammenfassung
    print("\n" + "=" * 60)
    print("📊 WORKFLOW ZUSAMMENFASSUNG")
    print("=" * 60)
    print(f"Produkt:          {product['title'][:40]}")
    print(f"Amazon Preis:     ${product['price']:.2f}")
    print(f"Lieferant:        {best_supplier}")
    print(f"Lieferantenpreis: ${supplier_price['price']:.2f}")
    print(f"Verkaufspreis:    ${selling_price:.2f}")
    print(f"Gewinn:           ${profit_info['profit']:.2f}")
    print(f"Margin:           {profit_info['margin_percent']:.1f}%")
    print(f"Bestellung:       {order['order_id']}")
    print(f"Status:           {fulfilled['status']}")
    print(f"Tracking:         {tracking}")
    print("\n✅ INTEGRATION TEST ERFOLGREICH!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_complete_workflow()
    except Exception as e:
        print(f"\n❌ TEST FEHLGESCHLAGEN: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
