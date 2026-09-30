import hashlib
import secrets

# In-memory active tokens
active_tokens = {}

def hash_password(password: str) -> str:
    """Hashes passwords using standard SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against the stored hash."""
    return hash_password(plain_password) == hashed_password

def generate_token(user_id: str, role: str) -> str:
    """Creates a session token for logged-in users."""
    token = secrets.token_hex(16)
    active_tokens[token] = {"user_id": user_id, "role": role}
    return token

def authenticate_session(token: str):
    """Fetches user details from session storage."""
    return active_tokens.get(token, None)
