import discord
from discord.ext import commands
from bot.config import TEST_GUILD_ID


class ClankerSentinel(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="/", intents=intents)

    async def setup_hook(self):
        await self.load_extension("bot.cogs.ping")
        print("loaded PingCog")

        # load cogs here

        guild = discord.Object(id=TEST_GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

    async def on_ready(self):
        print(f"Bot successfully logged in as {self.user}")
