# --- Middleware to strip /api prefix ---
class StripPrefixMiddleware:
  def __init__(self, app, prefix: str):
    self.app = app
    self.prefix = prefix.rstrip("/") or "/"

  async def __call__(self, scope, receive, send):
    if scope["type"] not in ("http", "websocket"):
      await self.app(scope, receive, send)
      return

    path = scope.get("path", "")
    if path == self.prefix:
      new_path = "/"
    elif path.startswith(self.prefix + "/"):
      new_path = path[len(self.prefix) :]
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
          new_scope["raw_path"] = raw[len(pb) :]
      except Exception:
        pass

    # Update root_path so docs and redirects include /api
    new_scope["root_path"] = new_scope.get("root_path", "") + self.prefix

    await self.app(new_scope, receive, send)
