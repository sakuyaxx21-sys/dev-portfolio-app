"""Seed script to create the initial admin user."""

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.users import User
from app.core.security import get_password_hash


def seed():
    """Create the default admin user if it does not exist."""
    db: Session = SessionLocal()

    try:
        # Check if the admin user already exists
        admin = db.query(User).filter(User.email == "admin@example.com").first()
        
        if admin:
            print("admin already exists")
            return
        
        # Create the initial admin user
        admin = User(
            name="Admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin12345"),
            role="admin",
        )
        
        db.add(admin)
        db.commit()
        
        print("admin user created")

    finally:
        # Ensure the DB session is always closed
        db.close()


if __name__ == "__main__":
    # Execute the seed script only when run directly
    seed()