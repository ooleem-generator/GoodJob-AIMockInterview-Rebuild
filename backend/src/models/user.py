from sqlmodel import SQLModel, Field
from datetime import datetime


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(primary_key=True)  # Clerk User ID (from JWT 'sub' claim)
    email: str = Field(unique=True, index=True)
    name: str | None = None
    email_verified: bool = Field(default=False)
    image_url: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
