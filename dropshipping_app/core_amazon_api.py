import os
import requests
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class AmazonAPI:
    def __init__(self):
        self.api_key = os.getenv("AMAZON_API_KEY", "demo_key")
        self.base_url = "https://api.amazon.com/v1"
        self.demo_mode = self.api_key == "demo_key"
    
    def search_products(self, query: str, category: str = None) -> List[Dict]:
        """Suche Produkte auf Amazon"""
        if self.demo_mode:
            return self._demo_search(query)
        
        try:
            params = {"keywords": query, "category": category}
            response = requests.get(f"{self.base_url}/search", params=params, timeout=5)
            return response.json().get("products", [])
        except Exception as e:
            print(f"Amazon API Error: {e}")
            return []
    
    def get_product_details(self, asin: str) -> Dict:
        """Hole Produktdetails"""
        if self.demo_mode:
            return self._demo_product_details(asin)
        
        try:
            response = requests.get(f"{self.base_url}/products/{asin}", timeout=5)
            return response.json()
        except Exception as e:
            print(f"Error fetching product: {e}")
            return {}
    
    def get_price_history(self, asin: str) -> List[Dict]:
        """Hole Preishistorie"""
        if self.demo_mode:
            return self._demo_price_history()
        
        try:
            response = requests.get(f"{self.base_url}/products/{asin}/pricing", timeout=5)
            return response.json().get("history", [])
        except Exception as e:
            return []
    
    def _demo_search(self, query: str) -> List[Dict]:
        return [
            {"asin": "B001", "title": f"Premium {query} - 100% Original", "price": 29.99, "rating": 4.8},
            {"asin": "B002", "title": f"Budget {query} - Best Value", "price": 14.99, "rating": 4.5},
            {"asin": "B003", "title": f"Professional {query} - Pro Edition", "price": 49.99, "rating": 4.9},
        ]
    
    def _demo_product_details(self, asin: str) -> Dict:
        return {
            "asin": asin,
            "title": "Demo Product",
            "price": 29.99,
            "rating": 4.7,
            "reviews": 1250,
            "stock": 500,
            "description": "High quality product with excellent reviews"
        }
    
    def _demo_price_history(self) -> List[Dict]:
        return [
            {"date": "2025-01-01", "price": 35.00},
            {"date": "2025-01-08", "price": 32.00},
            {"date": "2025-01-15", "price": 29.99},
        ]
