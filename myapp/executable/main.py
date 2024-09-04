import os

import fastapi
import fastapi.middleware.cors
import uvicorn

from myapp.executable import routes
from myapp.executable.common import State

router = fastapi.APIRouter()
router.include_router(routes.router, tags=["Requested Routes"])


@router.get("/health")
def get_health() -> fastapi.Response:
    return fastapi.Response()


def get_app_fastapi(state: State) -> fastapi.FastAPI:
    app = fastapi.FastAPI(
        title="Fastapi Events App",
        version="1.0",
    )
    app.state.mystate = state

    async def app_on_startup() -> None:
        state.logger.info("app_on_startup")

    async def app_on_shutdown() -> None:
        state.logger.info("app_on_shutdown")

    app.add_event_handler("startup", app_on_startup)
    app.add_event_handler("shutdown", app_on_shutdown)
    app.add_middleware(
        fastapi.middleware.cors.CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)

    return app


def main() -> None:
    state = State()
    app = get_app_fastapi(state)

    # Use * for both IPv4 and IPv6 addresses
    host = "*"
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
