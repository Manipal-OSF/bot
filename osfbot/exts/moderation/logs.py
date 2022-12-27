from datetime import datetime

from disnake import (
    ButtonStyle,
    Component,
    Embed,
    Member,
    Message,
    RawMessageDeleteEvent,
    TextChannel,
)
from disnake.ext.commands import Cog
from disnake.ui import Button
from disnake.utils import format_dt
from loguru import logger

from ...bot import Bot
from ...constants import Channels, Colors


class ModerationLogs(Cog):
    """Used to log infractions and important actions in the specified channel."""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.log_channel: TextChannel | None = None
        super().__init__()

    async def post_message(
        self,
        embed: Embed,
        components: list[Component] = None,
    ) -> Message | None:
        """Send the given message in the log channel."""
        if self.log_channel is None:
            await self.bot.wait_until_ready()
            self.log_channel = await self.bot.fetch_channel(Channels.log)

            if self.log_channel is None:
                logger.error(f"Failed to get log channel with ID ({Channels.log})")

        return await self.log_channel.send(embed=embed, components=components)

    async def post_formatted_message(
        self,
        actor: Member,
        title: str,
        color: int = Colors.green,
        fields: list | None = None,
        url: str | None = None,
        components: list[Component] = None,
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
            embed.add_field(
                name=field["name"], value=field["value"], inline=field["inline"]
            )

        await self.post_message(embed=embed, components=components)

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
                    "inline": False,
                },
                {
                    "name": "Channel",
                    "value": f"{message.channel.mention} **({message.channel.name}) ({message.channel.id})**",
                    "inline": False,
                },
                {
                    "name": "Content",
                    "value": f"```{message.content[:1000]+('...' if len(message.content) > 1024 else '')}```",
                    "inline": False,
                },
            ]

            await self.post_formatted_message(
                actor=message.author,
                title=f"Message Deleted ({message.id})",
                color=Colors.red,
                fields=fields,
            )

        else:
            channel = await self.bot.fetch_channel(payload.channel_id)

            await self.post_message(
                Embed(
                    title=f"Message Deleted ({payload.message_id})",
                    description=f"The message in {channel.mention} wasn't cached, and cannot be displayed.",
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
                "inline": False,
            },
            {
                "name": "Before",
                "value": f"```{before.content[:1000]+('...' if len(before.content) > 1024 else '')}```",
                "inline": False,
            },
            {
                "name": "After",
                "value": f"```{after.content[:1000]+('...' if len(after.content) > 1024 else '')}```",
                "inline": False,
            },
        ]

        components = [
            Button(
                style=ButtonStyle.link,
                label="Jump to message",
                url=after.jump_url,
            ),
        ]

        await self.post_formatted_message(
            actor=after.author,
            title=f"Message Edited ({after.id})",
            color=Colors.yellow,
            fields=fields,
            components=components,
        )

    @Cog.listener()
    async def on_member_join(self, member: Member) -> None:
        """Logs members joining."""
        fields = [
            {
                "name": "Name",
                "value": f"{member}",
                "inline": True,
            },
            {
                "name": "Profile",
                "value": f"{member.mention}",
                "inline": True,
            },
            {
                "name": "Account Created",
                "value": f"{format_dt(member.created_at)} ({format_dt(member.created_at, 'R')})",
                "inline": True,
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
                "inline": True,
            },
            {
                "name": "Profile",
                "value": f"{member.mention}",
                "inline": True,
            },
            {
                "name": "Account Created",
                "value": f"{format_dt(member.created_at)} ({format_dt(member.created_at, 'R')})",
                "inline": True,
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
                "inline": True,
            },
            {
                "name": "Before",
                "value": f"{before.nick}",
                "inline": True,
            },
            {
                "name": "After",
                "value": f"{after.nick}",
                "inline": True,
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
