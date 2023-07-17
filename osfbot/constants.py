import os
import pathlib
from typing import NamedTuple

ENVIRONMENT = os.getenv("ENVIRONMENT")
if ENVIRONMENT is None:
    from dotenv import load_dotenv

    load_dotenv(dotenv_path=f"{os.getcwd()}/.env")

# Environment Vars
PREFIX = os.getenv("PREFIX", ">")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Paths
EXTENSIONS = pathlib.Path("osfbot/exts/")

if TEST_GUILDS := os.getenv("TEST_GUILDS"):
    TEST_GUILDS = [int(x) for x in TEST_GUILDS.split(",")]


class Colors:
    blue = 0x3DB9C4
    green = 0x53B543
    orange = 0xF09600
    red = 0xE72B31
    yellow = 0xF3EA00
    client_dark = 0x303136
    client_light = 0xF2F3F5


class Channels(NamedTuple):
    devlog = int(os.getenv("CHANNEL_DEVLOG", 937615771276812330))
    log = int(os.getenv("CHANNEL_LOG", 937615771276812330))
    dmlog = int(os.getenv("CHANNEL_DMLOG", 937615771276812330))


class Roles(NamedTuple):
    moderator = int(os.getenv("ROLE_MODERATOR", 839527120354279474))
    osf_member = int(os.getenv("ROLE_OSF_MEMBER", 996267159577698364))
