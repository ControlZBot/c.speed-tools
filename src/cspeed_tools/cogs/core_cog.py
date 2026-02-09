from pathlib import Path
import yaml
import discord
from discord import app_commands
from discord.ext import commands


class CoreCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


def _build_generic_command(endpoint_path: str) -> app_commands.Command:
    command_name = endpoint_path.split("/")[-1]

    async def handler(interaction: discord.Interaction, _path: str = endpoint_path) -> None:
        await interaction.response.send_message(
            f"c.speed-tools executed {_path}. Configure modules if needed.",
            ephemeral=True,
        )

    return app_commands.Command(
        name=command_name,
        description=f"c.speed-tools {command_name}",
        callback=handler,
    )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CoreCog(bot))
    path = Path(__file__).resolve().parents[1] / "manifest" / "commands_manifest.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    top_groups: dict[str, app_commands.Group] = {}
    sub_groups: dict[tuple[str, str], app_commands.Group] = {}

    for endpoint in data["endpoints"]:
        endpoint_path = str(endpoint["path"])
        if endpoint_path.startswith("/owner/") or endpoint_path.startswith("/misc/"):
            continue
        parts = [part for part in endpoint_path.split("/") if part]
        if len(parts) == 2:
            top, command_name = parts
            if top not in top_groups:
                top_groups[top] = app_commands.Group(name=top, description=f"c.speed-tools {top}")
                bot.tree.add_command(top_groups[top])
            top_groups[top].add_command(_build_generic_command(endpoint_path))
            continue
        if len(parts) == 3:
            top, subgroup_name, _command_name = parts
            if top not in top_groups:
                top_groups[top] = app_commands.Group(name=top, description=f"c.speed-tools {top}")
                bot.tree.add_command(top_groups[top])
            key = (top, subgroup_name)
            if key not in sub_groups:
                sub_groups[key] = app_commands.Group(
                    name=subgroup_name,
                    description=f"c.speed-tools {subgroup_name}",
                )
                top_groups[top].add_command(sub_groups[key])
            sub_groups[key].add_command(_build_generic_command(endpoint_path))
