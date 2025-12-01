"""Authentication & Authorization"""
import jwt
import os
from datetime import datetime, timedelta
from typing import Dict

SECRET_KEY = os.getenv("JWT_SECRET", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"

def generate_token(user_id: str, role: str = "user", expires_in_hours: int = 24) -> str:
    """Generate JWT token"""
    payload = {
        "user_id": user_id,
        "role": role,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=expires_in_hours)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> Dict:
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")

def create_admin_token() -> str:
    """Create admin token for testing"""
    return generate_token("admin", role="admin", expires_in_hours=24)

def create_user_token(user_id: str) -> str:
    """Create user token"""
    return generate_token(user_id, role="user", expires_in_hours=24)

# Generate test tokens
if __name__ == "__main__":
    admin_token = create_admin_token()
    user_token = create_user_token("user1")
    
    print("🔐 Generated Tokens:")
    print(f"\nAdmin Token:\n{admin_token}")
    print(f"\nUser Token:\n{user_token}")
    print("\nUse with: Authorization: Bearer <token>")
