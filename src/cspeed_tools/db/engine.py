from __future__ import annotations

import aiosqlite
from pathlib import Path

class Database:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self._conn: aiosqlite.Connection | None = None

    async def connect(self) -> None:
        if self.database_url.startswith("sqlite"):
            path = self.database_url.split("///")[-1]
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            self._conn = await aiosqlite.connect(path)
            self._conn.row_factory = aiosqlite.Row
        else:
            raise RuntimeError("This build supports sqlite fallback runtime in CI/dev")

    @property
    def conn(self) -> aiosqlite.Connection:
        if self._conn is None:
            raise RuntimeError("DB not connected")
        return self._conn

    async def close(self) -> None:
        if self._conn:
            await self._conn.close()
