from sqlalchemy import create_engine, Integer, Column
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./local.db")

engine = create_engine(
  DATABASE_URL,
  connect_args={"check_same_thread": False}
  if DATABASE_URL.startswith("sqlite")
  else {},
)

SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
  pass


class BaseIdMixin:
  id: Mapped[int] = mapped_column(
    Integer, primary_key=True, index=True, autoincrement=True
  )


def get_db():
  """
  Yields a current DB Session. Can be used in a FastAPI Dependency.
  The Session is automatically closed after it is no longer needed.
  """
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
