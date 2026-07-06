from fastapi import FastAPI

from app.core.config import settings
from app.core.error_handlers import register_error_handlers
from app.core.logging import configure_logging


configure_logging()
app = FastAPI(title=settings.app_name)
register_error_handlers(app)
