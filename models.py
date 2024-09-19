from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from db import engine

class Base(DeclarativeBase):
  pass

class User(Base):
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(primary_key=True)
  password: Mapped[str] = mapped_column(String(64))
  public_key: Mapped[str]

class Entry(Base):
  __tablename__ = "entries"

  id: Mapped[int] = mapped_column(primary_key=True)
  service: Mapped[str]
  email: Mapped[str]
  password: Mapped[str]
  
  __table_args__ = (
    UniqueConstraint('email', 'service', name='unique_email_service'),
  )

Base.metadata.create_all(engine)