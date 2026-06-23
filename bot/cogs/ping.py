from discord import app_commands
from discord.ext import commands
from bot.config import DESCRIPTIONS


class PingCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(name="ping", description=DESCRIPTIONS["ping"])
    async def ping(self, interaction) -> None:
        await interaction.response.send_message(
            f"Gateway : {round(self.bot.latency * 1000)} ms"
        )


async def setup(bot) -> None:
    await bot.add_cog(PingCog(bot))
