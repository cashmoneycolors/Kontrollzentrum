from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import uvicorn

from core_amazon_api import AmazonAPI
from core_pricing_engine import PricingEngine
from core_order_manager import OrderManager, OrderStatus
from core_supplier_api import SupplierAPI

app = FastAPI(title="Amazon Dropshipping API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

amazon_api = AmazonAPI()
pricing_engine = PricingEngine()
order_manager = OrderManager()
supplier_api = SupplierAPI()

class SearchRequest(BaseModel):
    query: str
    category: str = None

class OrderRequest(BaseModel):
    customer_email: str
    items: List[Dict]
    total: float

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "dropshipping-api"}

@app.post("/search")
def search_products(request: SearchRequest):
    """Suche Produkte auf Amazon"""
    products = amazon_api.search_products(request.query, request.category)
    
    for product in products:
        supplier = supplier_api.get_best_supplier(product.get("asin"), 1)
        supplier_price = supplier_api.get_supplier_price(product.get("asin"), supplier)
        
        selling_price = pricing_engine.calculate_selling_price(supplier_price.get("price", 10))
        profit_info = pricing_engine.calculate_profit(supplier_price.get("price", 10), selling_price)
        
        product["supplier"] = supplier
        product["supplier_price"] = supplier_price.get("price")
        product["selling_price"] = selling_price
        product["profit"] = profit_info["profit"]
        product["margin"] = profit_info["margin_percent"]
    
    return {"products": products}

@app.get("/product/{asin}")
def get_product(asin: str):
    """Hole Produktdetails"""
    product = amazon_api.get_product_details(asin)
    price_history = amazon_api.get_price_history(asin)
    
    return {
        "product": product,
        "price_history": price_history
    }

@app.post("/orders")
def create_order(request: OrderRequest):
    """Erstelle neue Bestellung"""
    order = order_manager.create_order(request.customer_email, request.items, request.total)
    return order

@app.get("/orders/{order_id}")
def get_order(order_id: str):
    """Hole Bestelldetails"""
    order = order_manager.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.get("/orders/status/{status}")
def get_orders_by_status(status: str):
    """Hole Bestellungen nach Status"""
    try:
        order_status = OrderStatus(status)
        orders = order_manager.get_orders_by_status(order_status)
        return {"status": status, "orders": orders}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid status")

@app.post("/orders/{order_id}/fulfill")
def fulfill_order(order_id: str, supplier_tracking: str):
    """Automatische Fulfillment"""
    order = order_manager.auto_fulfill_order(order_id, supplier_tracking)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.get("/stats")
def get_stats():
    """Hole Statistiken"""
    pending = len(order_manager.get_pending_orders())
    shipped = len(order_manager.get_orders_by_status(OrderStatus.SHIPPED))
    delivered = len(order_manager.get_orders_by_status(OrderStatus.DELIVERED))
    
    return {
        "pending_orders": pending,
        "shipped_orders": shipped,
        "delivered_orders": delivered,
        "total_orders": len(order_manager.orders)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
