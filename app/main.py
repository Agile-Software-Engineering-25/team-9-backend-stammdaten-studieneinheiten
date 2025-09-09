from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
from app.core.db import Base, engine

# you need to import these so their models get registered
from app.models import course_template
from app.models import course

from app.models import module_templates
Base.metadata.drop_all(bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="team-9-backend-service")
app.include_router(api_router)

# Configure CORS
origins = [
  "http://localhost:5173",  # Vite default
  "http://127.0.0.1:5173",  # sometimes browser uses this
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],  # which origins are allowed
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
