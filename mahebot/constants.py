import os

from dotenv import load_dotenv

ENVIRONMENT = os.getenv("ENVIRONMENT")
if ENVIRONMENT is None:
    load_dotenv(dotenv_path=f"{os.getcwd()}/.env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
