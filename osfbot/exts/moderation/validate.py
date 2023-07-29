from datetime import datetime

from disnake import (
    ApplicationCommandInteraction,
    Embed,
    Member,
    Message,
    Role,
    TextChannel,
)
from disnake.ext.commands import Cog, slash_command
from loguru import logger

from ...bot import Bot
from ...constants import Channels, Colors, Roles

BASE_URL = "https://osf-database-api.shuttleapp.rs"


class OSFValidation(Cog):
    """Checks if user is OSF member on joining."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.log_channel: TextChannel | None = None
        self.osf_member: Role | None = None
        super().__init__()

    async def post_message(
        self,
        title: str,
        description: str,
        color: int = Colors.green,
    ) -> Message | None:
        """Sends the given message in the log channel."""
        if self.log_channel is None:
            await self.bot.wait_until_ready()
            self.log_channel = await self.bot.fetch_channel(Channels.log)

            if self.log_channel is None:
                logger.error(f"Failed to get log channel with ID ({Channels.log})")

        return await self.log_channel.send(
            embed=Embed(
                title=title,
                description=description,
                timestamp=datetime.now(),
                color=color,
            )
        )

    async def process_status(self, member: Member, status: bool | str) -> None:
        """Gives the OSF Member role to validated user."""
        if self.osf_member is None:
            await self.bot.wait_until_ready()
            self.osf_member = member.guild.get_role(Roles.osf_member)

            if self.osf_member is None:
                logger.error(
                    f"Failed to get OSF Member role with ID ({Roles.osf_member})"
                )

        if status and isinstance(status, bool):
            await member.add_roles(self.osf_member)
            await self.post_message(
                title=f"OSF Member Added ({member.id})",
                description=f"{member.mention} **({member.name}) ({member.id})** was validated by the bot.",
                color=Colors.green,
            )
        elif isinstance(status, str):
            await self.post_message(
                title=f"OSF Validation Error ({member.id})",
                description=f"```{status}```",
                color=Colors.red,
            )

    async def validate_status(self, id: int) -> bool | str:
        """Fetches member status from the OSF database."""
        async with self.bot.http_session.get(
            f"{BASE_URL}/api/v1/bot/validate",
            json={
                "id": id,
            },
        ) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data["result"]
            else:
                text = await resp.text()
                return f"{resp.status}: {text}"

    @Cog.listener()
    async def on_member_join(self, member: Member) -> None:
        """Validate user on joining the server."""
        status = await self.validate_status(member.id)
        await self.process_status(member, status)

    @slash_command()
    async def validate(
        self, itr: ApplicationCommandInteraction, member: Member = None
    ) -> None:
        """Command to validate users already in the server."""
        if not member:
            member = itr.user

        await itr.response.defer(ephemeral=True)

        status = await self.validate_status(member.id)
        await self.process_status(member, status)

        if isinstance(status, bool):
            if status is True:
                embed = Embed(
                    title=f"OSF Validation Successful ({member.id})",
                    description=f"{member.mention} was verified, and has been given the relevant roles.",
                    timestamp=datetime.now(),
                    color=Colors.green,
                )
            elif status is False:
                embed = Embed(
                    title=f"OSF Validation Failed ({member.id})",
                    description=f"Could not verify {member.mention} as a part of Manipal OSF.",
                    timestamp=datetime.now(),
                    color=Colors.orange,
                )
        else:
            embed = Embed(
                title=f"OSF Validation Error ({member.id})",
                description="Could not validate user. Moderators have been informed of the error.",
                timestamp=datetime.now(),
                color=Colors.red,
            )

        await itr.edit_original_response(embed=embed)


def setup(bot: Bot) -> None:
    """Loads the OSFValidation cog."""
    bot.add_cog(OSFValidation(bot))
