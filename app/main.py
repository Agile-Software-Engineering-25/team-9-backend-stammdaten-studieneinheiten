from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
from app.core.db import Base, engine

# you need to import these so their models get registered
from app.models import course_template
from app.models import course
from app.models import module_templates

# Base.metadata.drop_all(bind=engine) # de-comment this if you want to reset the database upon reload
Base.metadata.create_all(bind=engine)


# --- Middleware to strip /api prefix ---
class StripPrefixMiddleware:
    def __init__(self, app, prefix: str):
        self.app = app
        self.prefix = (prefix.rstrip('/') or '/')

    async def __call__(self, scope, receive, send):
        if scope['type'] not in ('http', 'websocket'):
            await self.app(scope, receive, send)
            return

        path = scope.get("path", "")
        if path == self.prefix:
            new_path = "/"
        elif path.startswith(self.prefix + "/"):
            new_path = path[len(self.prefix):]
        else:
            await self.app(scope, receive, send)
            return

        new_scope = dict(scope)
        new_scope["path"] = new_path

        raw = new_scope.get("raw_path")
        if raw is not None:
            try:
                pb = self.prefix.encode("utf-8")
                if raw == pb or raw == pb + b"/":
                    new_scope["raw_path"] = b"/"
                elif raw.startswith(pb + b"/"):
                    new_scope["raw_path"] = raw[len(pb):]
            except Exception:
                pass

        # Update root_path so docs and redirects include /api
        new_scope["root_path"] = new_scope.get("root_path", "") + self.prefix

        await self.app(new_scope, receive, send)


# Create FastAPI app
fastapi_app = FastAPI(title="team-9-backend-service")
fastapi_app.include_router(api_router)

# Configure CORS
origins = [
    "http://localhost:5173",  # Vite default
    "http://127.0.0.1:5173",  # sometimes browser uses this
]

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # which origins are allowed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Wrap the app with the prefix-stripping middleware
app = StripPrefixMiddleware(fastapi_app, prefix="/masterdata/studies")
