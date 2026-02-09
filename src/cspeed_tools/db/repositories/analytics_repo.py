from . import BaseRepository


class AnalyticsRepository(BaseRepository):
    async def increment_counter(self, key: str) -> str:
        return key
