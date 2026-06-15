from discord.ext import commands
from discord import app_commands


class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Botun ağ gecikmesini görüntüler")
    async def ping(self, interaction):
        await interaction.response.send_message(
            f"Gateway : {round(self.bot.latency * 1000)} ms"
        )


async def setup(bot):
    await bot.add_cog(PingCog(bot))
