from bot.services import database
from bot.services.database import Trigger
from discord.ext import commands
from discord import interaction
from discord.app_commands import app_commands


class TriggerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    autoresponse_group = app_commands.Group(
        name="autoresponse", description="Otomatik cevapları ekler, kaldırır ve yönetir"
    )

    @autoresponse_group.command(name="add", description="Otomatik cevap ekler")
    async def add_trigger(self, interaction):
        if database.query_triggers() is not None:
            await interaction.response.send_message(
                "Hata : Bu otomatik cevap onceden ayarlanmis"
            )
            return

        trigger = Trigger(
            interaction.guild.id,
        )
        database.add_trigger()

    @autoresponse_group.command(
        name="delete", description="Secilen otomatik cevabi siler"
    )
    async def delete_trigger():
        pass

    @autoresponse_group.command(
        name="state", description="Secilen otomatik cevabı acıp kapatır"
    )
    async def change_trigger_state():
        pass

    @autoresponse_group.command(
        name="listall", description="Tum otomatik cevaplari listeler"
    )
    async def list_triggers():
        pass

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:
            return
        if message.author.bot:
            return

        message_text = message.content.casefold().strip()
        trigger = Trigger(message.guild.id, message_text, None, None)
        response = database.query_triggers(self.bot.conn, trigger)

        if response is None:
            return

        await interaction.response.send_message(f"{response}")
