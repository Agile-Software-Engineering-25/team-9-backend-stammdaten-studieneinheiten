from sqlalchemy import create_engine, Integer, Column
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped
import os

IS_DEPLOYED = os.getenv("IS_DEPLOYED", "false").lower()=="true"

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    if IS_DEPLOYED:
        PG_HOST = os.getenv("DB_HOST", "postgres.db")  # K8s service name
        PG_PORT = os.getenv("DB_PORT", "5432")
        PG_DB   = os.getenv("DATABASE", "appdb")
        PG_USER = os.getenv("DB_USER", "appuser")
        PG_PASS = os.getenv("DB_PASSWORD", "error")
        DATABASE_URL = f"postgresql+psycopg2://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}"
    else:
        DATABASE_URL = "sqlite:///./local.db"


if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        future=True,  #not entirely sure what this is, but is apparently best practice
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # helps with stale connections in long-running pods
        future=True,
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
