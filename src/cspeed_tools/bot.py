import aiohttp
import discord
from discord.ext import commands


class ServiceContainer:
    def __init__(self, settings, db, global_actions_service):
        self.settings = settings
        self.db = db
        self.global_actions_service = global_actions_service


class CSpeedBot(commands.Bot):
    def __init__(self, container: ServiceContainer):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(command_prefix="!", intents=intents)
        self.container = container
        self.http_session: aiohttp.ClientSession | None = None

    async def setup_hook(self) -> None:
        self.http_session = aiohttp.ClientSession()
        modules = [
            "cspeed_tools.cogs.core_cog",
            "cspeed_tools.cogs.owner_cog",
            "cspeed_tools.cogs.misc_cog",
            "cspeed_tools.cogs.moderation_cog",
            "cspeed_tools.cogs.automod_cog",
            "cspeed_tools.cogs.cases_cog",
            "cspeed_tools.cogs.logs_cog",
            "cspeed_tools.cogs.server_cog",
            "cspeed_tools.cogs.channels_cog",
            "cspeed_tools.cogs.roles_cog",
            "cspeed_tools.cogs.members_cog",
            "cspeed_tools.cogs.tickets_cog",
            "cspeed_tools.cogs.levels_cog",
            "cspeed_tools.cogs.economy_cog",
            "cspeed_tools.cogs.fun_cog",
            "cspeed_tools.cogs.games_cog",
            "cspeed_tools.cogs.utility_cog",
            "cspeed_tools.cogs.reminders_cog",
            "cspeed_tools.cogs.welcome_cog",
            "cspeed_tools.cogs.verification_cog",
            "cspeed_tools.cogs.starboard_cog",
            "cspeed_tools.cogs.polls_cog",
            "cspeed_tools.cogs.giveaways_cog",
            "cspeed_tools.cogs.announcements_cog",
            "cspeed_tools.cogs.tags_cog",
            "cspeed_tools.cogs.profiles_cog",
            "cspeed_tools.cogs.voice_cog",
            "cspeed_tools.cogs.music_cog",
            "cspeed_tools.cogs.images_cog",
            "cspeed_tools.cogs.staff_cog",
            "cspeed_tools.cogs.antiabuse_cog",
            "cspeed_tools.cogs.integrations_cog",
            "cspeed_tools.cogs.backup_cog",
            "cspeed_tools.cogs.analytics_cog",
            "cspeed_tools.cogs.dev_cog",
        ]
        for module in modules:
            await self.load_extension(module)

        dev_guild_id = self.container.settings.dev_guild_id
        if dev_guild_id:
            dev_guild = discord.Object(id=dev_guild_id)
            self.tree.clear_commands(guild=dev_guild)
            await self.tree.sync(guild=dev_guild)
        else:
            await self.tree.sync()

    async def on_member_join(self, member: discord.Member) -> None:
        await self.container.global_actions_service.enforce_on_join(member)

    async def close(self) -> None:
        if self.http_session:
            await self.http_session.close()
        await super().close()
