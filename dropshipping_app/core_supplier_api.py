import os
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class SupplierAPI:
    def __init__(self):
        self.api_key = os.getenv("SUPPLIER_API_KEY", "demo_key")
        self.demo_mode = self.api_key == "demo_key"
        self.suppliers = {
            "alibaba": {"name": "Alibaba", "shipping_days": 14, "min_order": 1},
            "dhgate": {"name": "DHGate", "shipping_days": 10, "min_order": 1},
            "1688": {"name": "1688", "shipping_days": 7, "min_order": 5}
        }
    
    def get_supplier_price(self, product_id: str, supplier: str = "alibaba") -> Dict:
        """Hole Lieferantenpreis"""
        if self.demo_mode:
            return self._demo_supplier_price(supplier)
        
        # Real API call would go here
        return {}
    
    def place_supplier_order(self, supplier: str, items: List[Dict], shipping_address: str) -> Dict:
        """Platziere Bestellung beim Lieferanten"""
        if self.demo_mode:
            return self._demo_order_placement(supplier, items)
        
        return {}
    
    def get_supplier_tracking(self, order_id: str, supplier: str) -> str:
        """Hole Tracking-Nummer vom Lieferanten"""
        if self.demo_mode:
            return f"TRACK-{supplier.upper()}-{order_id}"
        
        return ""
    
    def _demo_supplier_price(self, supplier: str) -> Dict:
        prices = {
            "alibaba": {"price": 8.50, "shipping": 2.00, "lead_time": 14},
            "dhgate": {"price": 9.00, "shipping": 1.50, "lead_time": 10},
            "1688": {"price": 7.50, "shipping": 3.00, "lead_time": 7}
        }
        return prices.get(supplier, prices["alibaba"])
    
    def _demo_order_placement(self, supplier: str, items: List[Dict]) -> Dict:
        return {
            "supplier_order_id": f"SUP-{supplier.upper()}-12345",
            "status": "confirmed",
            "estimated_delivery": "2025-02-15",
            "tracking": f"TRACK-{supplier.upper()}-12345"
        }
    
    def get_best_supplier(self, product_id: str, quantity: int) -> str:
        """Finde besten Lieferanten basierend auf Preis und Lieferzeit"""
        best_supplier = "alibaba"
        best_price = float('inf')
        
        for supplier in self.suppliers.keys():
            price_info = self.get_supplier_price(product_id, supplier)
            if price_info.get("price", float('inf')) < best_price:
                best_price = price_info.get("price")
                best_supplier = supplier
        
        return best_supplier
