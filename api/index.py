import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import app as fastapi_app


class StripApiPrefix:
    """Vercel routes the raw /api/* path to this function; strip it so the
    underlying FastAPI routes (unprefixed, same as behind nginx) still match."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and scope["path"].startswith("/api"):
            scope["path"] = scope["path"][len("/api"):] or "/"
        await self.app(scope, receive, send)


app = StripApiPrefix(fastapi_app)
