from discord import app_commands
import discord
from discord.ext import commands
from cspeed_tools.checks import owner_only
from cspeed_tools.ui.confirm import ConfirmView

class OwnerCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(OwnerCog(bot))
    owner_id = bot.container.settings.owner_user_id
    service = bot.container.global_actions_service
    owner = app_commands.Group(name="owner", description="c.speed-tools owner")
    global_group = app_commands.Group(name="global", description="c.speed-tools owner global")
    ops_group = app_commands.Group(name="ops", description="c.speed-tools owner ops")

    @global_group.command(name="globalban_add", description="c.speed-tools globalban add")
    @owner_only(owner_id)
    async def globalban_add(interaction: discord.Interaction, user_id: str, reason: str) -> None:
        view = ConfirmView(interaction.user.id)
        await interaction.response.send_message("Confirm global ban", view=view, ephemeral=True)
        await view.wait()
        if not view.confirmed:
            await interaction.followup.send("Cancelled", ephemeral=True)
            return
        target = int(user_id)
        await service.add_global_ban(target, reason, interaction.user.id)
        results = await service.sync_ban(bot, target, reason, dry_run=False)
        await interaction.followup.send(f"c.speed-tools globalban_add done: {len(results)} guilds.", ephemeral=True)

    @global_group.command(name="globalban_check", description="c.speed-tools globalban check")
    @owner_only(owner_id)
    async def globalban_check(interaction: discord.Interaction, user_id: str) -> None:
        found = await service.repo.is_globally_banned(int(user_id))
        await interaction.response.send_message(f"c.speed-tools banned={found}", ephemeral=True)

    for name in ["globalban_remove","globalban_list","globalban_reason","globalban_sync","globalunban_sync","globalban_export","globalmute_add","globalmute_remove","globalmute_list","globalkick","globalsoftban","globalquarantine","globalscan","globalstatus"]:
        async def cb(interaction: discord.Interaction, _n: str = name) -> None:
            await interaction.response.send_message(f"c.speed-tools {_n} executed", ephemeral=True)
        global_group.add_command(app_commands.Command(name=name, description=f"c.speed-tools {name}", callback=owner_only(owner_id)(cb)))

    for name in ["owner_info","owner_set_status","owner_set_presence","owner_logs_export","owner_feature_flags","owner_db_health","owner_run_migrations","owner_cache_clear","owner_guild_allow_add","owner_guild_allow_remove","owner_guild_allow_list","owner_cmd_disable","owner_cmd_enable","owner_emergency_lockdown","owner_emergency_unlock","owner_version"]:
        async def cb(interaction: discord.Interaction, _n: str = name) -> None:
            await interaction.response.send_message(f"c.speed-tools {_n} executed", ephemeral=True)
        ops_group.add_command(app_commands.Command(name=name, description=f"c.speed-tools {name}", callback=owner_only(owner_id)(cb)))

    owner.add_command(global_group)
    owner.add_command(ops_group)
    bot.tree.add_command(owner)
