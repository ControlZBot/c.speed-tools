from dataclasses import dataclass
import discord
from cspeed_tools.db.repositories.global_actions_repo import GlobalActionsRepository

@dataclass(slots=True)
class GuildActionResult:
    guild_id: int
    ok: bool
    detail: str

class GlobalActionsService:
    def __init__(self, repo: GlobalActionsRepository):
        self.repo = repo

    async def add_global_ban(self, user_id: int, reason: str, actor_id: int) -> None:
        await self.repo.add_global_ban(user_id, reason, actor_id)

    async def sync_ban(self, bot: discord.Client, user_id: int, reason: str, dry_run: bool) -> list[GuildActionResult]:
        results = []
        for guild in bot.guilds:
            if dry_run:
                results.append(GuildActionResult(guild.id, True, "dry-run"))
                continue
            try:
                await guild.ban(discord.Object(id=user_id), reason=reason)
                results.append(GuildActionResult(guild.id, True, "banned"))
            except discord.Forbidden:
                results.append(GuildActionResult(guild.id, False, "missing_permissions"))
            except discord.HTTPException as exc:
                results.append(GuildActionResult(guild.id, False, str(exc)))
        return results
