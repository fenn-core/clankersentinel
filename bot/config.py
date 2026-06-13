from dotenv import load_dotenv
from os import getenv
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

env_path = ROOT_DIR / ".env"
load_dotenv(env_path)


TOKEN = getenv("TOKEN")

if TOKEN is None:
    raise KeyError


TEST_GUILD_ID = int(getenv("TEST_GUILD_ID"))

if TEST_GUILD_ID is None:
    raise KeyError
