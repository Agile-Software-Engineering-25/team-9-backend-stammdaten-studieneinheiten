from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
from app.core.db import Base, engine
from app.core.middleware import StripPrefixMiddleware

# you need to import these so their models get registered
from app.models import course_template
from app.models import course
from app.models import module_templates
from app.models import courseofstudy_templates
from app.models import module

import os

is_deployed = os.getenv("IS_DEPLOYED", "false").lower()=="true"

# Base.metadata.drop_all(bind=engine) # de-comment this if you want to reset the database upon reload
Base.metadata.create_all(bind=engine)


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
app = StripPrefixMiddleware(fastapi_app, prefix="/masterdata/studies")
