import os
import pathlib

ENVIRONMENT = os.getenv("ENVIRONMENT")
if ENVIRONMENT is None:
    from dotenv import load_dotenv

    load_dotenv(dotenv_path=f"{os.getcwd()}/.env")

# Environment Vars
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Paths
EXTENSIONS = pathlib.Path("osfbot/exts/")
