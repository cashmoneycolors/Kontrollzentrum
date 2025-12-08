"""
API-Key Validierung - Optional (Demo-Modus wenn Keys fehlen)
"""
import os
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

OPTIONAL_KEYS = [
    "OPENAI_API_KEY",
    "STRIPE_API_KEY",
    "PAYPAL_CLIENT_ID",
    "AWS_ACCESS_KEY_ID",
    "NFT_API_KEY",
]

REQUIRED_KEYS = OPTIONAL_KEYS

def check_all_keys():
    """Prüft ob mindestens ein API-Key vorhanden ist - Demo-Modus wenn nicht"""
    available = [k for k in OPTIONAL_KEYS if os.getenv(k)]
    if not available:
        print("⚠️  Keine API-Keys gefunden - Demo-Modus aktiviert")
    return True

def require_keys(func):
    """Decorator: Optional - nutzt Keys wenn vorhanden, sonst Demo"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        check_all_keys()
        return func(*args, **kwargs)
    return wrapper

def has_key(key_name):
    """Prüft ob ein spezifischer Key vorhanden ist"""
    return bool(os.getenv(key_name))

def get_available_keys():
    """Gibt Liste der verfügbaren Keys zurück"""
    return [k for k in OPTIONAL_KEYS if os.getenv(k)]
