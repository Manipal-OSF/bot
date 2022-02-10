from disnake import Intents
from disnake.ext import commands
from osfbot import constants


class Bot(commands.Bot):
    """The core of the bot."""

    def __init__(self) -> None:
        intents = Intents.default()
        intents.members = True
        intents.presences = True

        super().__init__(command_prefix=">")

    def run(self) -> None:
        """Run the bot with token present in .env."""
        if constants.BOT_TOKEN is None:
            raise EnvironmentError(
                "Token value is None. Make sure you have configured the TOKEN field in .env"
            )

        super().run(constants.BOT_TOKEN)

    async def on_ready(self) -> None:
        """Runs the bot when connected to discord and is ready."""
        print("Bot ready!")

    async def close(self) -> None:
        """Close the bot gracefully."""
        await super().close()
