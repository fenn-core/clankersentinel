from bot.services import database
from bot.services.database import User
from discord.ext import commands
from discord import app_commands
from time import time


class StatsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_voice_sessions = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:
            return
        if message.author.bot:
            return

        user = User(message.guild.id, message.id)
        database.ensure_user(self.bot.conn, user)
        database.increment_message_count(self.bot.conn, user)

    # fix the channel switching bug

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.guild is None:
            return

        user_data = (member.guild.id, member.id)

        if (before.channel is None) and (after.channel is not None):
            self.active_voice_sessions[user_data] = time()

        if (before.channel is not None) and (after.channel is None):
            elapsed_time = time() - self.active_voice_sessions[user_data]
            user = User(member.guild.id, member.id)
            database.ensure_user(self.bot.conn, user)
            database.record_voice_session(self.bot.conn, user, elapsed_time)

    @app_commands.command(
        name="rank",
        description="Seviye, deneyim ve aktivite istatistiklerini görüntüler",
    )
    async def rank(self, interaction):
        user = User(interaction.guild.id, interaction.user.id)
        database.ensure_user(self.bot.conn, user)

        await interaction.response.send_message("rank feature under development")

    @app_commands.command(
        name="leaderboard",
        description="Sunucudaki en aktif kullanıcıları sıralar",
    )
    async def leaderboard(self, interaction):
        await interaction.response.send_message("leaderboard feature under development")


async def setup(bot):
    await bot.add_cog(StatsCog(bot))
