import json
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


DATABASE_PATH = ROOT_DIR / "bot" / "data" / "clankersentinel.db"

if DATABASE_PATH is None:
    raise KeyError


with open("config.json", "r") as config:
    dicts = json.load(config)

DESCRIPTIONS = dicts["descriptions"]
EMBED_ELEMENTS = dicts["embed_elements"]
FEEDBACK = dicts["feedback"]


def info(message):
    print(f"\033[92m[INFO]\033[0m {message}")


def warning(message):
    print(f"\033[93m[WARNING]\033[0m {message}")


def error(message):
    print(f"\033[91m[ERROR]\033[0m {message}")


def debug(message):
    print(f"\033[96m[DEBUG]\033[0m {message}")


def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    parts = []
    if hours:
        parts.append(f"{hours}h")
    if minutes or not parts:
        parts.append(f"{minutes}m")

    formatted_time = " ".join(parts)

    return formatted_time
