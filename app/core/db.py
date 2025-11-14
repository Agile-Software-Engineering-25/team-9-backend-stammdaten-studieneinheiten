import os
from sqlalchemy import create_engine, Integer, Column
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped
from sqlalchemy.engine import URL
from sqlalchemy import MetaData, event
import traceback

IS_DEPLOYED = os.getenv("IS_DEPLOYED", "false").lower() == "true"
DATABASE_URL = os.getenv("DATABASE_URL")

DEFAULT_SCHEMA = os.getenv("BASE_SCHEMA")  # keep the hyphen

if not DATABASE_URL:
  if IS_DEPLOYED:
    PG_HOST = os.getenv(
      "DB_HOST", "postgres.db"
    )  # If app is in a different ns, include the namespace, e.g. postgres.db
    PG_PORT = int(os.getenv("DB_PORT", "5432"))
    PG_DB = os.getenv("DATABASE", "appdb")
    PG_USER = os.getenv("DB_USER", "appuser")
    PG_PASS = os.getenv("DB_PASSWORD", "error")

    DATABASE_URL = URL.create(
      "postgresql+pg8000",
      username=PG_USER,
      password=PG_PASS,
      host=PG_HOST,
      port=PG_PORT,
      database=PG_DB,
    )
  else:
    DATABASE_URL = "sqlite:///./local.db"

if str(DATABASE_URL).startswith("sqlite"):
  engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True,  # not entirely sure what this is, but is apparently best practice
  )
else:
  engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # helps with stale connections in long-running pods
    future=True,  # not entirely sure what this is, but is apparently best practice
  )


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
  if not IS_DEPLOYED:
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
  if IS_DEPLOYED:
    metadata = MetaData(schema="ase-9_schema")
  else:
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
  except Exception as e:
    print("There was an error!")
    print(f"Type: {type(e).__name__}")
    print(f"Message: {e}")
    print("Traceback:")
    traceback.print_exc()
  finally:
    print("db closed")
    db.close()
