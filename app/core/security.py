"""Security utilities for JWT handling and password hashing."""

import hashlib

from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

from app.core.config import settings


def create_access_token(email: str) -> str:
    """Create a JWT access token with expiration."""
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    # JWT payload (subject = user email)
    payload = {
        "sub": email,
        "exp": expire,
    }
    
    token = jwt.encode(
        payload, 
        settings.secret_key, 
        algorithm=settings.algorithm,
    )

    return token


def verify_token(token: str) -> str | None:
    """Decode JWT and return email if valid, otherwise None."""
    try:
        payload = jwt.decode(
            token, 
            settings.secret_key, 
            algorithms=[settings.algorithm],
        )

        # Extract subject (email)
        email = payload.get("sub")
        if not isinstance(email, str):
            return None
        
        return email
    
    except JWTError:
        # Invalid or expired token
        return None


def get_password_hash(password: str) -> str:
    """Generate SHA256 hash from a plain password."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, hashed_password: str) -> bool:
    """Compare a plain password with the stored hash."""
    return get_password_hash(password) == hashed_password