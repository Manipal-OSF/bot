from datetime import datetime
from typing import Optional, Union

from disnake import Embed, Forbidden, Member, Message, TextChannel, User
from disnake.ext.commands import Cog, Context, command, has_any_role
from loguru import logger

from ...bot import Bot
from ...constants import Channels, Colors, Roles


class DirectMessages(Cog):
    """Used to send and receive DMs via the bot user."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.dm_log_channel: Optional[TextChannel] = None
        super().__init__()

    async def post_message(self, embed: Embed) -> Optional[Message]:
        """Send the given message in the DM log channel."""
        if not self.dm_log_channel:
            await self.bot.wait_until_ready()
            self.dm_log_channel = await self.bot.fetch_channel(Channels.dmlog)

            if not self.dm_log_channel:
                logger.error(f"Failed to get log channel with ID ({Channels.dmlog})")

        return await self.dm_log_channel.send(embed=embed)

    async def dm_message(
        self,
        author: Union[Member, User],
        receiver: Union[Member, User],
        color: int = Colors.client_dark,
        message: str = "<N/A>",
    ) -> None:
        """Formats an embed to display the corresponding DM."""
        embed = Embed(
            description=message,
            color=color,
            timestamp=datetime.now(),
        )

        embed.set_author(name=f"{author} ({author.id})", icon_url=author.avatar.url)
        embed.set_footer(
            text=f"{author.name} -> {receiver.name}", icon_url=receiver.avatar.url
        )

        await self.post_message(embed=embed)

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        """Logs incoming DMs to the specified log channel."""
        if message.guild:
            return

        await self.dm_message(
            author=message.author, receiver=self.bot.user, message=message.content
        )

    @command(aliases=("dm",))
    @has_any_role(Roles.moderator)
    async def message(self, ctx: Context, user: Member, *, message: str) -> None:
        """Send a DM to a specified user."""
        logger.info(f"Sending message {message!r} to {user}")

        try:
            await user.send(message)
            await ctx.message.delete()

            await self.dm_message(author=ctx.author, receiver=user, message=message)
        except Forbidden:
            await ctx.message.add_reaction("\N{CROSS MARK}")

            await self.post_message(
                Embed(
                    title="DM Failed", color=Colors.red, timestamp=datetime.now()
                ).set_footer(
                    text=f"{ctx.author} -> {user}", icon_url=ctx.author.avatar.url
                )
            )


def setup(bot: Bot) -> None:
    """Loads the DirectMessages cog."""
    bot.add_cog(DirectMessages(bot))
