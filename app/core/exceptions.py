"""W10：統一錯誤格式。前端只看到 error／path，不看到 Python traceback。"""

from __future__ import annotations

import logging

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("app")


class AppException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


def _error_body(request: Request, message: str) -> dict:
    return {"error": message, "path": request.url.path}


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    logger.error(
        "AppException %s %s → %s",
        request.method,
        request.url.path,
        exc.message,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_body(request, exc.message),
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """既有 HTTPException 也走同一 JSON 形狀（不必一次改完全部 raise）。"""
    detail = exc.detail
    if isinstance(detail, (list, dict)):
        message = str(detail)
    else:
        message = str(detail)
    if exc.status_code >= 500:
        logger.error("HTTPException %s %s → %s", request.method, request.url.path, message)
    else:
        logger.info("HTTPException %s %s → %s", request.method, request.url.path, message)
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_body(request, message),
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """未預期例外：log 完整 stack，回應不洩漏細節。"""
    logger.exception(
        "Unhandled error on %s %s",
        request.method,
        request.url.path,
    )
    return JSONResponse(
        status_code=500,
        content=_error_body(request, "Internal server error"),
    )
