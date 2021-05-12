import asyncpg
from typing import Optional


class SessionStorage:
    _pool: Optional[asyncpg.Pool] = None

    async def connect(self, dsn: str):
        if not self._pool:
            self._pool = await asyncpg.create_pool(dsn)

    @classmethod
    def get_pool(cls) -> asyncpg.Pool:
        if not cls._pool:
            raise Exception("Orm is not connected to db")

        return cls._pool
