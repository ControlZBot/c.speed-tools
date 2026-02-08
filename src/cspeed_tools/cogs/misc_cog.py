import base64
import hashlib
import json
import uuid as uuid_mod
from discord import app_commands
import discord
from discord.ext import commands

class MiscCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MiscCog(bot))
    misc = app_commands.Group(name="misc", description="c.speed-tools misc")
    tools = app_commands.Group(name="tools", description="c.speed-tools tools")
    extras = app_commands.Group(name="extras", description="c.speed-tools extras")

    @tools.command(name="uuid", description="c.speed-tools uuid")
    async def uuid_cmd(interaction: discord.Interaction) -> None:
        await interaction.response.send_message(str(uuid_mod.uuid4()), ephemeral=True)

    @tools.command(name="base64", description="c.speed-tools base64")
    async def base64_cmd(interaction: discord.Interaction, text: str) -> None:
        await interaction.response.send_message(base64.b64encode(text.encode()).decode(), ephemeral=True)

    @tools.command(name="hash", description="c.speed-tools hash")
    async def hash_cmd(interaction: discord.Interaction, text: str) -> None:
        await interaction.response.send_message(hashlib.sha256(text.encode()).hexdigest(), ephemeral=True)

    @tools.command(name="json_validate", description="c.speed-tools json_validate")
    async def json_validate(interaction: discord.Interaction, payload: str) -> None:
        try:
            json.loads(payload)
            msg = "valid"
        except json.JSONDecodeError as exc:
            msg = f"invalid: {exc}"
        await interaction.response.send_message(msg, ephemeral=True)

    for name in ["paste","whois","id","snowflake_time","color_convert","ping_raw","perms_diag","rate_limits","markdown_escape","text_diff","timezones"]:
        async def cb(interaction: discord.Interaction, _n: str = name) -> None:
            await interaction.response.send_message(f"c.speed-tools {_n}", ephemeral=True)
        tools.add_command(app_commands.Command(name=name, description=f"c.speed-tools {name}", callback=cb))

    for name in ["afk_set","afk_clear","afk_status","quicknote_add","quicknote_list","quicknote_del","template_add","template_list","template_del","cleanlinks","roleping_check","channel_health","message_stats","mini_backup","mini_restore"]:
        async def cb(interaction: discord.Interaction, _n: str = name) -> None:
            await interaction.response.send_message(f"c.speed-tools {_n}", ephemeral=True)
        extras.add_command(app_commands.Command(name=name, description=f"c.speed-tools {name}", callback=cb))

    misc.add_command(tools)
    misc.add_command(extras)
    bot.tree.add_command(misc)
