import asyncio
import os

from disnake import AllowedMentions, Embed, Intents
from disnake.ext import commands
from disnake.utils import utcnow
from osfbot import constants


class Bot(commands.Bot):
    """The core of the bot."""

    def __init__(self) -> None:
        intents = Intents.default()
        intents.members = True
        intents.presences = True

        test_guilds = None
        if constants.TEST_GUILDS:
            test_guilds = constants.TEST_GUILDS

        super().__init__(
            command_prefix=constants.PREFIX,
            intents=intents,
            test_guilds=test_guilds,
            allowed_mentions=AllowedMentions(
                everyone=None,
                users=True,
                replied_user=True,
            ),
        )

        self.initiated = False

    def load_extensions(self) -> None:
        """Load all the extensions in the exts/ folder."""
        for extension in constants.EXTENSIONS.glob("*/*.py"):
            if extension.name.startswith("_"):
                continue  # Ignore files starting with _
            ext_path = str(extension).replace(os.sep, ".")[:-3]  # Truncate .py
            self.load_extension(ext_path)
            print(f"Extension loaded: {ext_path}")

    def run(self) -> None:
        """Run the bot with token present in .env."""
        if constants.BOT_TOKEN is None:
            raise EnvironmentError(
                "Token value is None. Make sure you have configured the TOKEN field in .env"
            )

        super().run(constants.BOT_TOKEN)

    async def on_ready(self) -> None:
        """Runs the bot when connected to Discord and is ready."""
        if not self.initiated:
            await asyncio.sleep(2)
            self.load_extensions()
            await self.startup_alert()
            self.initiated = True
        print("The bot is online!")

    async def startup_alert(self) -> None:
        """Announce bot's presence to the devlog channel."""
        embed = Embed(
            title="Bot Startup",
            description="The bot is back online!",
            color=constants.Colors.green,
            timestamp=utcnow(),
        )
        await self.get_channel(constants.Channels.devlog).send(embed=embed)

    async def close(self) -> None:
        """Close the bot gracefully."""
        await super().close()
