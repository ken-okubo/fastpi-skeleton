#!/usr/bin/env python3
"""
Script to create an admin user.
Usage: python scripts/create_admin.py
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from getpass import getpass

from app.core.db import SessionLocal
from app.crud.user import create_user, get_user_by_email
from app.models.user import Role
from app.schemas.user import UserCreate

# Import all models so SQLAlchemy can resolve relationships
from app.models import user  # noqa: F401


def main():
    print("=== Create Admin User ===\n")

    email = input("Email: ").strip()
    if not email:
        print("Error: Email is required")
        return

    password = getpass("Password: ")
    if len(password) < 8:
        print("Error: Password must be at least 8 characters")
        return

    password_confirm = getpass("Confirm password: ")
    if password != password_confirm:
        print("Error: Passwords do not match")
        return

    db = SessionLocal()
    try:
        existing = get_user_by_email(db, email)
        if existing:
            print(f"Error: User with email '{email}' already exists")
            return

        user_data = UserCreate(
            email=email,
            password=password,
            roles=[Role.admin],
        )
        user = create_user(db, user_data)
        print(f"\nAdmin user created successfully!")
        print(f"ID: {user.id}")
        print(f"Email: {user.email}")
        print(f"Roles: {list(user.role_names)}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
