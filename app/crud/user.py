from typing import Optional
from uuid import UUID

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import Role, User, UserRole, UserStatus
from app.schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_user(
    db: Session,
    data: UserCreate,
    roles: Optional[list[Role]] = None,
) -> User:
    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        name=data.name,
    )
    db.add(user)
    db.flush()

    # Add roles
    role_list = roles if roles else data.roles
    for role in role_list:
        user_role = UserRole(user_id=user.id, role=role)
        db.add(user_role)

    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(db: Session, user_id: UUID) -> Optional[User]:
    return db.get(User, user_id)


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalar_one_or_none()


def authenticate_user(
    db: Session, email: str, password: str
) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    if user.status != UserStatus.active:
        return None
    return user


def update_password(db: Session, user: User, new_password: str) -> User:
    user.hashed_password = hash_password(new_password)
    db.commit()
    db.refresh(user)
    return user
