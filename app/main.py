from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
from app.core.db import Base, engine
from app.core.middleware import StripPrefixMiddleware

from alembic import command
from alembic.config import Config

import os

is_deployed = os.getenv("IS_DEPLOYED", "false").lower() == "true"

# Migrate Database
cfg = Config("alembic.ini")
command.upgrade(cfg, "head")

# Create FastAPI app
fastapi_app = FastAPI(title="team-9-backend-service")
fastapi_app.include_router(api_router)

origins = []
# Configure CORS
if not is_deployed:
  origins = [
    "http://localhost:5173",  # Vite default
    "http://127.0.0.1:5173",  # sometimes browser uses this
  ]
else:
  origins = []

fastapi_app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],  # which origins are allowed
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


# Wrap the app with the prefix-stripping middleware
app = StripPrefixMiddleware(fastapi_app, prefix="/api/masterdata/studies")
