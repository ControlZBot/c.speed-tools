import time
from cspeed_tools.db.repositories.levels_repo import LevelsRepository


class LevelService:
    def __init__(self, repo: LevelsRepository, cooldown_seconds: int = 30):
        self.repo = repo
        self.cooldown_seconds = cooldown_seconds

    async def award_message_xp(self, guild_id: int, user_id: int, amount: int = 5, now: float | None = None) -> int:
        event_ts = time.time() if now is None else now
        last = await self.repo.get_last_award_ts(guild_id, user_id)
        if event_ts - last < self.cooldown_seconds:
            return await self.repo.get_xp(guild_id, user_id)
        return await self.repo.add_xp(guild_id, user_id, amount, event_ts)
