from bot.services import database
from bot.services.database import User
from bot.config import warning
from bot.config import format_time
import discord
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

        user = User(message.guild.id, message.author.id)
        database.ensure_user(self.bot.conn, user)
        database.increment_message_count(self.bot.conn, user)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.guild is None:
            return

        user_data = (member.guild.id, member.id)

        if (before.channel is None) and (after.channel is not None):
            self.active_voice_sessions[user_data] = time()

        if (before.channel is not None) and (after.channel is None):
            join_time = self.active_voice_sessions.get(user_data)
            if join_time is None:
                warning(
                    f"couldn't retrieve voice chat join time for user {member.name}"
                )
                return
            elapsed_time = time() - join_time
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
        user.message_count, user.voice_seconds = database.query_user_stats(
            self.bot.conn, user
        )

        embed = discord.Embed(
            title=f"{interaction.user.name}'s Server Stats", color=discord.Color.blue()
        )
        embed.add_field(name="Level", value=user.level, inline=True)
        embed.add_field(name="Text Level", value=user.text_level, inline=True)
        embed.add_field(name="Voice Level", value=user.voice_level, inline=True)

        embed.add_field(name="Total XP", value=user.total_xp, inline=True)
        embed.add_field(name="Text XP", value=user.text_xp, inline=True)
        embed.add_field(name="Voice XP", value=user.voice_xp, inline=True)

        embed.add_field(name="Messages", value=user.message_count, inline=True)
        embed.add_field(
            name="Voice Time", value=format_time(user.voice_seconds), inline=True
        )

        await interaction.response.send_message(embed=embed)
        user.message_count = 0
        user.voice_seconds = 0

        # the formatting used here is temporary,
        # a image based output system will be implemented in the future

    leaderboard_group = app_commands.Group(
        name="leaderboard", description="Sunucudaki en aktif kullanıcıları sıralar"
    )

    @leaderboard_group.command(
        name="text", description="Sunucuda en çok mesaj atan kullanıcıları sıralar"
    )
    async def text(self, interaction: discord.Interaction):

        text_top5 = database.retrieve_top5_text_users(
            self.bot.conn, interaction.guild.id
        )

        if not text_top5:
            return await interaction.response.send_message(
                "Henüz mesaj verisi bulunmuyor."
            )

        leaderboard = ""

        for rank, (user_id, message_count) in enumerate(text_top5, start=1):
            member = interaction.guild.get_member(user_id)

            if member:
                name = member.display_name
            else:
                user = await self.bot.fetch_user(user_id)
                name = user.name

            leaderboard += f"**#{rank}** {name} • {message_count} messages\n"

        embed = discord.Embed(
            title="🏆 Text Leaderboard 🏆",
            description=leaderboard,
            color=discord.Color.blue(),
        )

        await interaction.response.send_message(embed=embed)

    @leaderboard_group.command(
        name="voice",
        description="Sunucudaki en yuksek sesli suresine sahip kullanıcıları sıralar",
    )
    async def voice(self, interaction: discord.Interaction):

        voice_top5 = database.retrieve_top5_voice_users(
            self.bot.conn, interaction.guild.id
        )

        if not voice_top5:
            return await interaction.response.send_message(
                "Henüz sesli verisi bulunmuyor."
            )

        leaderboard = ""

        for rank, (user_id, user_voice_time) in enumerate(voice_top5, start=1):
            formatted_time = format_time(user_voice_time)
            member = interaction.guild.get_member(user_id)

            if member:
                name = member.display_name
            else:
                user = await self.bot.fetch_user(user_id)
                name = user.name

            leaderboard += f"**#{rank}** {name} • {formatted_time} \n"

        embed = discord.Embed(
            title="🏆 Voice Leaderboard 🏆",
            description=leaderboard,
            color=discord.Color.blue(),
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(StatsCog(bot))
