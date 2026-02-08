from pathlib import Path
import yaml
from discord import app_commands
import discord
from discord.ext import commands

class CoreCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CoreCog(bot))
    path = Path(__file__).resolve().parents[1] / "manifest" / "commands_manifest.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    groups = {}
    for endpoint in [e for e in data["endpoints"] if str(e["top"]).startswith("group")]:
        top = endpoint["top"]
        cmd = endpoint["path"].split("/")[-1]
        if top not in groups:
            groups[top] = app_commands.Group(name=top, description=f"c.speed-tools {top}")
            bot.tree.add_command(groups[top])
        async def handler(interaction: discord.Interaction, _cmd: str = cmd) -> None:
            await interaction.response.send_message(f"c.speed-tools {_cmd} executed.", ephemeral=True)
        groups[top].add_command(app_commands.Command(name=cmd, description=f"c.speed-tools {cmd}", callback=handler))
