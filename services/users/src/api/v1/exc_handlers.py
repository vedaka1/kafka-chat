import logging

from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

from src.domain.exceptions import ApplicationException

logger = logging.getLogger()


async def app_exc_handler(
    request: Request, exc: ApplicationException
) -> ORJSONResponse:
    logger.error(msg="Handle error", exc_info=exc, extra={"error": exc})
    return ORJSONResponse(
        status_code=exc.status_code,
        content={"ok": False, "error_code": exc.status_code, "detail": exc.message},
    )


async def unknown_exception_handler(request: Request, err: Exception) -> ORJSONResponse:
    logger.error(msg="Handle error", exc_info=err, extra={"error": err})
    return ORJSONResponse(
        status_code=500,
        content={"ok": False, "error_code": 500, "detail": "Unknown error occurred"},
    )


def init_exc_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ApplicationException, app_exc_handler)
