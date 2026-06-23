from discord import app_commands
from discord.ext import commands
from bot.services import database
from bot.services.database import Trigger
from bot.config import (
    DESCRIPTIONS,
    FEEDBACK,
)

AUTORESPONSE_DESC = DESCRIPTIONS["autoresponse"]
AUTORESPONSE_FEEDBACK = FEEDBACK["autoresponse"]


class TriggerCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    autoresponse_group = app_commands.Group(
        name="autoresponse", description=AUTORESPONSE_DESC["group"]
    )

    @autoresponse_group.command(
        name="add", description=AUTORESPONSE_DESC["add"]["group"]
    )
    @app_commands.describe(
        trigger=AUTORESPONSE_DESC["add"]["trigger"],
        response=AUTORESPONSE_DESC["add"]["response"],
    )
    async def add_trigger(self, interaction, trigger: str, response: str) -> None:
        trigger_obj: Trigger = Trigger(interaction.guild.id, trigger, response, True)

        if database.query_triggers(self.bot.conn, trigger_obj) is not None:
            await interaction.response.send_message(AUTORESPONSE_FEEDBACK["exists"])
            return

        database.add_trigger(self.bot.conn, trigger_obj)
        await interaction.response.send_message(AUTORESPONSE_FEEDBACK["added"])

    @autoresponse_group.command(name="delete", description=AUTORESPONSE_DESC["delete"])
    async def delete_trigger(self, interaction, trigger: str) -> None:
        trigger_obj: Trigger = Trigger(interaction.guild.id, trigger, None, None)
        deleted = database.delete_triggers(self.bot.conn, trigger_obj)

        if deleted:
            await interaction.response.send_message(AUTORESPONSE_FEEDBACK["deleted"])
            return

        await interaction.response.send_message(AUTORESPONSE_FEEDBACK["not_found"])

    @autoresponse_group.command(name="state", description=AUTORESPONSE_DESC["state"])
    async def change_trigger_state(self, interaction, trigger: str, status: bool):
        trigger_obj: Trigger = Trigger(interaction.guild.id, trigger, None, None)
        changed = database.change_trigger_state(self.bot.conn, trigger_obj, status)

        if changed:
            await interaction.response.send_message(
                AUTORESPONSE_FEEDBACK["changed_state"]
            )
            return

        await interaction.response.send_message(AUTORESPONSE_FEEDBACK["not_found"])

    @autoresponse_group.command(
        name="listall", description=AUTORESPONSE_DESC["listall"]
    )
    async def list_triggers(self, interaction):
        all_values = database.query_all_triggers(self.bot.conn, interaction.guild.id)

        if not all_values:
            await interaction.response.send_message(AUTORESPONSE_FEEDBACK["not_found"])
            return

        formatted_output = "Trigger  ->  Response \n\n"
        for value in all_values:
            formatted_output += f"{value[0]}  ->  {value[1]} \n"

        await interaction.response.send_message(f"```{formatted_output}```")

    @commands.Cog.listener()
    async def on_message(self, message) -> None:
        if message.guild is None:
            return
        if message.author.bot:
            return

        message_text = message.content.casefold().strip()
        trigger: Trigger = Trigger(message.guild.id, message_text, None, None)
        response = database.query_triggers(self.bot.conn, trigger)

        if response is None:
            return

        (response,) = response  # unpack the single variable tuple
        await message.channel.send(f"{response}")


async def setup(bot) -> None:
    await bot.add_cog(TriggerCog(bot))
