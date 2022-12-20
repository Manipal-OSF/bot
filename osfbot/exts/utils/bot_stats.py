import disnake
from disnake.ext import commands


class BotStats(commands.Cog):
    """Information and statistics about the bot."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(3, 15)
    async def ping(self, ctx: commands.Context) -> None:
        """Returns the latency of the bot."""
        embed = disnake.Embed(
            title="Pong!",
            description=f"Gateway Latency: {round(self.bot.latency*1000)}ms",
        )
        await ctx.send(embed=embed)


def setup(bot: commands.Bot) -> None:
    """Loads the BotStats cog."""
    bot.add_cog(BotStats(bot))
