from datetime import datetime
from typing import Optional

from disnake import Embed, Member, Message, RawMessageDeleteEvent, TextChannel
from disnake.ext.commands import Cog
from disnake.utils import format_dt
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
        actor: Member,
        title: str,
        color: int = Colors.green,
        fields: Optional[list] = None,
        url: Optional[str] = None,
    ) -> None:
        """Formats an embed to be posted in the log channel."""
        embed = Embed(
            title=title,
            color=color,
            timestamp=datetime.now(),
        ).set_thumbnail(url=actor.display_avatar.url)

        if url:
            embed.url = url

        for field in fields:
            embed.add_field(name=field["name"], value=field["value"])

        await self.post_message(embed=embed)

    @Cog.listener()
    async def on_raw_message_delete(self, payload: RawMessageDeleteEvent) -> None:
        """Logs message deletion."""
        if message := payload.cached_message:
            if message.author.bot:
                return

            fields = [
                {
                    "name": "Author",
                    "value": f"{message.author.mention} **({message.author.name}) ({message.author.id})**",
                },
                {
                    "name": "Channel",
                    "value": f"{message.channel.mention} **({message.channel.name}) ({message.channel.id})**",
                },
                {
                    "name": "Content",
                    "value": f"```{message.content[:1000]+('...' if len(message.content) > 1024 else '')}```",
                },
            ]

            await self.post_formatted_message(
                actor=message.author,
                title=f"Message Deleted ({message.id})",
                color=Colors.red,
                fields=fields,
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

    @Cog.listener()
    async def on_message_edit(self, before: Message, after: Message) -> None:
        """Logs message edits."""
        if after.author.bot or before.content == after.content:
            return

        fields = [
            {
                "name": "Author",
                "value": f"{after.author.mention} **({after.author.name}) ({after.author.id})**",
            },
            {
                "name": "Before",
                "value": f"```{before.content[:1000]+('...' if len(before.content) > 1024 else '')}```",
            },
            {
                "name": "After",
                "value": f"```{after.content[:1000]+('...' if len(after.content) > 1024 else '')}```",
            },
        ]

        await self.post_formatted_message(
            actor=after.author,
            title=f"Message Edited ({after.id})",
            color=Colors.yellow,
            fields=fields,
            url=after.jump_url,
        )

    @Cog.listener()
    async def on_member_join(self, member: Member) -> None:
        """Logs members joining."""
        fields = [
            {
                "name": "Name",
                "value": f"{member}",
            },
            {
                "name": "Profile",
                "value": f"{member.mention}",
            },
            {
                "name": "Account Created",
                "value": f"{format_dt(member.created_at)} ({format_dt(member.created_at, 'R')})",
            },
        ]

        await self.post_formatted_message(
            actor=member,
            title=f"Member Joined ({member.id})",
            fields=fields,
        )

    @Cog.listener()
    async def on_member_remove(self, member: Member) -> None:
        """Logs members leaving."""
        fields = [
            {
                "name": "Name",
                "value": f"{member}",
            },
            {
                "name": "Profile",
                "value": f"{member.mention}",
            },
            {
                "name": "Account Created",
                "value": f"{format_dt(member.created_at)} ({format_dt(member.created_at, 'R')})",
            },
        ]

        await self.post_formatted_message(
            actor=member,
            title=f"Member Left ({member.id})",
            color=Colors.red,
            fields=fields,
        )

    @Cog.listener()
    async def on_member_update(self, before: Member, after: Member) -> None:
        """Logs nickname changes."""
        if before.nick == after.nick:
            return

        fields = [
            {
                "name": "Profile",
                "value": f"{after.mention}",
            },
            {
                "name": "Before",
                "value": f"{before.nick}",
            },
            {
                "name": "After",
                "value": f"{after.nick}",
            },
        ]

        await self.post_formatted_message(
            actor=after,
            title=f"Nickname Updated ({after.id})",
            color=Colors.blue,
            fields=fields,
        )


def setup(bot: Bot) -> None:
    """Loads the ModerationLogs cog."""
    bot.add_cog(ModerationLogs(bot))
