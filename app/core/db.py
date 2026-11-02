"""
W08：連線池。

- 同步：`get_connection()` → ConnectionPool（repositories 共用）
- 非同步：`get_async_connection()` → AsyncConnectionPool（notes 示範）

不要每次 API 都 `psycopg.connect()` 開新連線；用完歸還池子。
"""
from __future__ import annotations

import os

from dotenv import load_dotenv
from psycopg_pool import AsyncConnectionPool, ConnectionPool

load_dotenv()

_pool: ConnectionPool | None = None
_async_pool: AsyncConnectionPool | None = None


def _database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set. Create a local .env file.")
    return database_url


def _pool_bounds() -> tuple[int, int]:
    min_size = int(os.getenv("DB_POOL_MIN_SIZE", "1"))
    max_size = int(os.getenv("DB_POOL_MAX_SIZE", "10"))
    if min_size < 1 or max_size < min_size:
        raise RuntimeError("DB_POOL_MIN_SIZE / DB_POOL_MAX_SIZE are invalid")
    return min_size, max_size


def init_sync_pool() -> ConnectionPool:
    global _pool
    if _pool is not None:
        return _pool
    min_size, max_size = _pool_bounds()
    _pool = ConnectionPool(
        conninfo=_database_url(),
        min_size=min_size,
        max_size=max_size,
        open=True,
        name="fastapi-sync",
    )
    return _pool


async def init_async_pool() -> AsyncConnectionPool:
    global _async_pool
    if _async_pool is not None:
        return _async_pool
    min_size, max_size = _pool_bounds()
    _async_pool = AsyncConnectionPool(
        conninfo=_database_url(),
        min_size=min_size,
        max_size=max_size,
        open=False,
        name="fastapi-async",
    )
    await _async_pool.open()
    return _async_pool


def close_sync_pool() -> None:
    global _pool
    if _pool is not None:
        _pool.close()
        _pool = None


async def close_async_pool() -> None:
    global _async_pool
    if _async_pool is not None:
        await _async_pool.close()
        _async_pool = None


def get_connection():
    """回傳 pool 的 connection context manager：`with get_connection() as conn:`。"""
    return init_sync_pool().connection()


def get_async_connection():
    """回傳 async pool 的 connection context manager。"""
    if _async_pool is None:
        raise RuntimeError("Async pool is not initialized. App lifespan must call init_async_pool().")
    return _async_pool.connection()
