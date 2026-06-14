from bot.config import TEST_GUILD_ID
from bot.config import info, error
import discord
from discord.ext import commands
from bot.services import database
from time import time
from asyncio import sleep


class ClankerSentinel(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="/", intents=intents)
        self.conn = None
        self.startup_time = None

    async def uptime(self):
        sleep(300)
        info(f"uptime : {time() - self.startup_time}")

    async def setup_hook(self):
        self.conn = database.initialize()
        if self.conn is None:
            error("database initialization failed")
            return
        info("initialized database")

        await self.load_extension("bot.cogs.ping")
        info("loaded PingCog")
        await self.load_extension("bot.cogs.stats")
        info("loaded StatsCog")

        guild = discord.Object(id=TEST_GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

        self.startup_time = time()

    async def on_ready(self):
        info(f"Bot successfully logged in as {self.user}")
