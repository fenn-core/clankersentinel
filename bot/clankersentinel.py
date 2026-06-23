from typing import NoReturn

import discord
from discord.ext import commands
from time import time
from asyncio import sleep, create_task
from bot.services import database
from bot.config import (
    TEST_GUILD_ID,
    format_time,
    info,
    error,
)


class ClankerSentinel(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="/", intents=intents)
        self.conn = None
        self.startup_time = None
        self.uptime_task = None

    async def uptime(self) -> NoReturn:
        while True:
            await sleep(300)
            info(f"uptime : {format_time(time() - self.startup_time)}")

    async def setup_hook(self) -> None:
        self.conn = database.initialize()
        if self.conn is None:
            error("database initialization failed")
            return
        info("initialized database")

        await self.load_extension("bot.cogs.ping")
        info("loaded PingCog")
        await self.load_extension("bot.cogs.stats")
        info("loaded StatsCog")
        await self.load_extension("bot.cogs.trigger")
        info("loaded TriggerCog")

        guild = discord.Object(id=TEST_GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

        self.startup_time = time()

    async def on_ready(self) -> None:
        info(f"Bot successfully logged in as {self.user}")

        if self.uptime_task is None:
            self.uptime_task = create_task(self.uptime())
