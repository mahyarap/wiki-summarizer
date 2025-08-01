from contextlib import asynccontextmanager

from fastapi import FastAPI

from .config import Settings
from .routes import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # This is here to fail early if the API key is not present
    app.state.settings = Settings() # type: ignore[reportCallIssue]
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Wikipedia Agent", lifespan=lifespan)
    app.include_router(api_router)
    return app


app = create_app()
