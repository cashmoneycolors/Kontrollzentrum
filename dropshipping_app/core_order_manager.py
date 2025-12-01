from datetime import datetime
from typing import List, Dict
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderManager:
    def __init__(self):
        self.orders = {}
        self.order_counter = 1000
    
    def create_order(self, customer_email: str, items: List[Dict], total: float) -> Dict:
        """Erstelle neue Bestellung"""
        order_id = f"ORD-{self.order_counter}"
        self.order_counter += 1
        
        order = {
            "order_id": order_id,
            "customer_email": customer_email,
            "items": items,
            "total": total,
            "status": OrderStatus.PENDING,
            "created_at": datetime.now().isoformat(),
            "tracking": None
        }
        
        self.orders[order_id] = order
        return order
    
    def update_order_status(self, order_id: str, status: OrderStatus, tracking: str = None) -> Dict:
        """Update Bestellstatus"""
        if order_id in self.orders:
            self.orders[order_id]["status"] = status
            if tracking:
                self.orders[order_id]["tracking"] = tracking
            return self.orders[order_id]
        return {}
    
    def get_order(self, order_id: str) -> Dict:
        """Hole Bestelldetails"""
        return self.orders.get(order_id, {})
    
    def get_orders_by_status(self, status: OrderStatus) -> List[Dict]:
        """Hole alle Bestellungen mit Status"""
        return [o for o in self.orders.values() if o["status"] == status]
    
    def get_pending_orders(self) -> List[Dict]:
        """Hole ausstehende Bestellungen"""
        return self.get_orders_by_status(OrderStatus.PENDING)
    
    def auto_fulfill_order(self, order_id: str, supplier_tracking: str) -> Dict:
        """Automatische Fulfillment"""
        return self.update_order_status(order_id, OrderStatus.SHIPPED, supplier_tracking)
