from discord.ext import commands
from services.translation import translate_to_english
from config import SETTINGS

SOURCE_ANN_CHANNEL_ID = SETTINGS["translation"]["source_ann_channel_id"]
OUTPUT_ANN_CHANNEL_ID = SETTINGS["translation"]["output_ann_channel_id"]


class AnnouncementTranslationCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message) -> None:  # translate bot msgs aswell
        if message.guild is None:
            return
        if message.channel.id != SOURCE_ANN_CHANNEL_ID:
            return
        if not message.content.strip():
            return

        translated_msg: str = await translate_to_english(message.content)

        channel = self.bot.get_channel(OUTPUT_ANN_CHANNEL_ID)

        if channel is None:
            channel = await self.bot.fetch_channel(OUTPUT_ANN_CHANNEL_ID)

        await channel.send(translated_msg)


async def setup(bot) -> None:
    if SOURCE_ANN_CHANNEL_ID == OUTPUT_ANN_CHANNEL_ID:
        raise ValueError("Translation source and output channels cannot be the same")

    await bot.add_cog(AnnouncementTranslationCog(bot))
