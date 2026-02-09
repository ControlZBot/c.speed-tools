from cspeed_tools.db.repositories.guild_config_repo import GuildConfigRepository


class GuildConfigService:
    def __init__(self, repo: GuildConfigRepository):
        self.repo = repo

    async def ensure_guild(self, guild_id: int) -> int:
        return await self.repo.ensure_guild(guild_id)
