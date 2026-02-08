from discord.ext import commands

class StarboardCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(StarboardCog(bot))
