from . import BaseRepository


class GuildConfigRepository(BaseRepository):
    async def ensure_guild(self, guild_id: int) -> int:
        return int(guild_id)
