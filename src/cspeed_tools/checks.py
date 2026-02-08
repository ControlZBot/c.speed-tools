import discord
from discord import app_commands

def owner_only(owner_id: int):
    async def predicate(interaction: discord.Interaction) -> bool:
        if interaction.user.id != owner_id:
            raise app_commands.CheckFailure("Owner-only command")
        return True
    return app_commands.check(predicate)
