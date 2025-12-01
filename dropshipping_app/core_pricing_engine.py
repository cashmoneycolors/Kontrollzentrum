from typing import Dict

class PricingEngine:
    def __init__(self, target_margin: float = 0.35):
        self.target_margin = target_margin
        self.shipping_cost = 2.50
        self.platform_fee = 0.15
    
    def calculate_selling_price(self, cost: float) -> float:
        """Berechne Verkaufspreis basierend auf Kosten und Margin"""
        total_costs = cost + self.shipping_cost + self.platform_fee
        selling_price = total_costs / (1 - self.target_margin)
        return round(selling_price, 2)
    
    def calculate_profit(self, cost: float, selling_price: float) -> Dict:
        """Berechne Gewinn und Margin"""
        total_costs = cost + self.shipping_cost + self.platform_fee
        profit = selling_price - total_costs
        margin = (profit / selling_price) * 100 if selling_price > 0 else 0
        
        return {
            "cost": cost,
            "shipping": self.shipping_cost,
            "platform_fee": self.platform_fee,
            "total_cost": total_costs,
            "selling_price": selling_price,
            "profit": round(profit, 2),
            "margin_percent": round(margin, 2)
        }
    
    def get_competitive_price(self, market_price: float, competitor_count: int = 3) -> float:
        """Berechne wettbewerbsfähigen Preis"""
        discount = 0.02 * (competitor_count - 1)
        return round(market_price * (1 - discount), 2)
