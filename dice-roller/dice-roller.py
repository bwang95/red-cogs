import discord
import re
from discord.ext import commands
from random import randint

class DiceRoller:
    """D&D Dice Roller!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def dnd(self, ctx, dice = 'd20'):
        """
        Rolls a number composed of dice (1d20 + 1d8 + 4, etc.).
        Defaults to a d20.

        Accepted Characters: 1-9, +, -, d.

        """
        sanitized_string = re.sub('[^0-9d\+\-]', '', dice.lower())
        order_of_operators = re.sub('[^\+\-]', '', sanitized_string)
        dice = re.split('[\+\-]', sanitized_string)
        rolls = []
        for die in dice:
            # Append a 1 to the dice if there isn't a modifier
            if die[0] == 'd':
                die = '1' + die

            # Split it up into components
            components = list(map(lambda x: int(x), die.split('d')))
            length = len(components)

            # Vet formatting
            if length > 2:
                await self.bot.say("{} looks like {} isn't formatted right...".format(author.mention, die))
                return

            # If the length of the array is one, just add the number
            if length == 1:
                rolls.append(components[0])
            # Otherwise, roll the dice
            else:
                rolls.append(randint(1, components[1]))

        # Compose the result
        result = "{} ".format(rolls[0])
        total = rolls[0]
        for (index, roll) in enumerate(rolls[1:]):
            operator = order_of_operators[index]
            if operator == '+':
                total += roll
            elif operator == '-':
                total -= roll
            result += "{} {}".format(operator, roll)
        result += " {}".format(rolls[-1])
        await self.bot.say("{} {} = {}".format(ctx.message.author.mention, result, total))

def setup(bot):
    bot.add_cog(DiceRoller(bot))
