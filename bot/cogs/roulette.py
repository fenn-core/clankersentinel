from discord import app_commands
from random import randint
from typing import Literal
from config import DESCRIPTIONS, FEEDBACK

ROULETTE_FEEDBACK = FEEDBACK["roulette"]


class RouletteCog:
    def __init__(self, bot) -> None:
        self.bot = bot

    def spin(self) -> Literal["green"] | Literal["red"] | Literal["black"]:
        """
        Spins the roulette wheel with odds:

        Black : 49 %

        Red : 49 %

        Green : 2 %

        """

        rng = randint(1, 10_000)

        if rng <= 200:
            return "green"

        elif rng <= 5100:
            return "red"

        else:
            return "black"

    @app_commands.command(name="bet", description=DESCRIPTIONS["bet"])
    async def place_bet(self, interaction):







        # await interaction.response.send_message(
        #     ROULETTE_FEEDBACK["bet_placed"].format(
        #         color=placed_color, amount=bet_amount, balance=current_balance
        #     )
        # )


# roulette outputs text for now, the final version
# will make custom videos portraying a wheel spinning
