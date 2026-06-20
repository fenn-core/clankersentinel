from bot.services import database
from bot.services.database import Trigger
from discord.ext import commands
from discord import app_commands


class TriggerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    autoresponse_group = app_commands.Group(
        name="autoresponse", description="Otomatik cevapları ekler, kaldırır ve yönetir"
    )

    @autoresponse_group.command(name="add", description="Otomatik cevap ekler")
    @app_commands.describe(
        trigger="Botun tetikleneceği kelime veya cümle",
        response="Botun vereceği yanıt ",
    )
    async def add_trigger(self, interaction, trigger: str, response: str):
        trigger_obj = Trigger(interaction.guild.id, trigger, response, True)

        if database.query_triggers(self.bot.conn, trigger_obj) is not None:
            await interaction.response.send_message(
                "Hata : Bu otomatik cevap onceden ayarlanmis"
            )
            return

        database.add_trigger(self.bot.conn, trigger_obj)
        await interaction.response.send_message("Otomatik mesaj eklendi")

    @autoresponse_group.command(
        name="delete", description="Secilen otomatik cevabi siler"
    )
    async def delete_trigger(self, interaction, trigger: str):
        trigger_obj = Trigger(interaction.guild.id, trigger, None, None)
        deleted = database.delete_triggers(self.bot.conn, trigger_obj)

        if deleted:
            await interaction.response.send_message("Otomatik cevap silindi")
            return

        await interaction.response.send_message("Hata : Otomatik cevap bulunamadi")

    @autoresponse_group.command(
        name="state", description="Secilen otomatik cevabı acıp kapatır"
    )
    async def change_trigger_state(self, interaction, trigger: str, status: bool):
        trigger_obj = Trigger(interaction.guild.id, trigger, None, None)
        changed = database.change_trigger_state(self.bot.conn, trigger_obj, status)

        if changed:
            await interaction.response.send_message(
                "Otomatik cevap durumu degistirildi"
            )
            return

        await interaction.response.send_message("Hata : Otomatik cevap bulunamadi")

    @autoresponse_group.command(
        name="listall", description="Tum otomatik cevaplari listeler"
    )
    async def list_triggers(self, interaction):
        all_values = database.query_all_triggers(self.bot.conn, interaction.guild.id)

        if not all_values:
            await interaction.response.send_message(
                "Hata : Listelenecek otomatik cevap bulunamadi"
            )
            return

        formatted_output = "Trigger  ->  Response \n\n"
        for value in all_values:
            formatted_output += f"{value[0]}  ->  {value[1]} \n"

        await interaction.response.send_message(f"```{formatted_output}```")

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

        (response,) = response  # unpack the single variable tuple
        await message.channel.send(f"{response}")


async def setup(bot):
    await bot.add_cog(TriggerCog(bot))
