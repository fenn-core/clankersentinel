from discord.ext import commands
from discord import app_commands


class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Prints out test message")
    async def ping(self, interaction):
        await interaction.response.send_message("Test-Message 1234 - AbCd")


async def setup(bot):
    await bot.add_cog(PingCog(bot))
