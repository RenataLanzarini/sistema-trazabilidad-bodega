from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.v1.router import router as api_v1_router
from app.core.config import settings
from app.core.error_handlers import register_error_handlers
from app.core.logging import configure_logging


configure_logging()
app = FastAPI(title=settings.app_name)
register_error_handlers(app)
app.include_router(health_router)
app.include_router(api_v1_router, prefix=settings.api_v1_prefix)
