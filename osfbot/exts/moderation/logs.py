from datetime import datetime
from typing import Optional

from disnake import Embed, Message, RawMessageDeleteEvent, TextChannel, User
from disnake.ext.commands import Cog
from loguru import logger

from ...bot import Bot
from ...constants import Channels, Colors


class ModerationLogs(Cog):
    """Used to log infractions and important actions in the specified channel."""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.log_channel: Optional[TextChannel] = None
        super().__init__()

    async def post_message(self, embed: Embed) -> Optional[Message]:
        """Send the given message in the log channel."""
        if not self.log_channel:
            await self.bot.wait_until_ready()
            self.log_channel = await self.bot.fetch_channel(Channels.log)

            if not self.log_channel:
                logger.error(f"Failed to get log channel with ID ({Channels.log})")

        return await self.log_channel.send(embed=embed)

    async def post_formatted_message(
        self,
        actor: User,
        action: str,
        body: Optional[str] = None,
        link: Optional[str] = None,
        color: int = Colors.green,
    ) -> None:
        """Format an embed to be posted in the log channel."""
        logger.trace(f"Creating log {actor.id} {action}")

        embed = Embed(
            title=(
                f"{actor} "
                f"{f'({actor.display_name}) ' if actor.display_name != actor.name else ''}"
                f"({actor.id}) {action}"  # Display actor's display name/username accordingly.
            ),
            description=body or "<N/A>",
            color=color,
            timestamp=datetime.utcnow(),
        ).set_thumbnail(url=actor.display_avatar.url)

        if link:
            embed.url = link

        await self.post_message(embed=embed)

    @Cog.listener()
    async def on_raw_message_delete(self, payload: RawMessageDeleteEvent) -> None:
        """Logs message deletion."""
        if message := payload.cached_message:
            if message.author.bot:
                return

            await self.post_formatted_message(
                message.author,
                f"deleted a message in {message.channel}",
                body=message.content[:1024],
                color=Colors.red,
            )
        else:
            await self.post_message(
                Embed(
                    title=(
                        f"Message ID ({payload.message_id}) deleted in "
                        f"{await self.bot.fetch_channel(payload.channel_id)}."
                    ),
                    description="The message wasn't cached, and cannot be displayed.",
                    color=Colors.red,
                )
            )


def setup(bot: Bot) -> None:
    """Loads the ModerationLogs cog."""
    bot.add_cog(ModerationLogs(bot))
