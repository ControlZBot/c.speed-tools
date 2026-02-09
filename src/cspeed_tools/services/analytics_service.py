from cspeed_tools.db.repositories.analytics_repo import AnalyticsRepository


class AnalyticsService:
    def __init__(self, repo: AnalyticsRepository):
        self.repo = repo

    async def record_event(self, event_name: str) -> str:
        return await self.repo.increment_counter(event_name)
