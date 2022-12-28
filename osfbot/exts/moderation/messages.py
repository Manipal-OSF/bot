from datetime import datetime

from disnake import (
    ApplicationCommandInteraction,
    Embed,
    Forbidden,
    Member,
    Message,
    TextChannel,
    User,
)
from disnake.ext.commands import Cog, has_any_role, slash_command
from loguru import logger

from ...bot import Bot
from ...constants import Channels, Colors, Roles


class DirectMessages(Cog):
    """Used to send and receive DMs via the bot user."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.dm_log_channel: TextChannel | None = None
        super().__init__()

    async def post_message(self, embed: Embed) -> Message | None:
        """Send the given message in the DM log channel."""
        if self.dm_log_channel is None:
            await self.bot.wait_until_ready()
            self.dm_log_channel = await self.bot.fetch_channel(Channels.dmlog)

            if self.dm_log_channel is None:
                logger.error(f"Failed to get log channel with ID ({Channels.dmlog})")

        return await self.dm_log_channel.send(embed=embed)

    async def dm_message(
        self,
        author: Member | User,
        receiver: Member | User,
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
        if message.guild or message.author == self.bot.user:
            return

        await self.dm_message(
            author=message.author, receiver=self.bot.user, message=message.content
        )

    @slash_command()
    @has_any_role(Roles.moderator)
    async def message(
        self, itr: ApplicationCommandInteraction, user: Member, *, message: str
    ) -> None:
        """Allows moderators to DM specific users."""
        logger.info(f"Sending message {message!r} to {user}")

        await itr.response.defer(ephemeral=True)

        try:
            await user.send(message)
            await itr.edit_original_response("DM Sent.")
            await self.dm_message(author=itr.author, receiver=user, message=message)
        except Forbidden:
            await itr.edit_original_response(
                embed=Embed(
                    title="DM Failed", color=Colors.red, timestamp=datetime.now()
                ).set_footer(
                    text=f"{itr.author} -> {user}", icon_url=itr.author.avatar.url
                )
            )


def setup(bot: Bot) -> None:
    """Loads the DirectMessages cog."""
    bot.add_cog(DirectMessages(bot))
