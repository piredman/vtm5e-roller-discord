# bot.py
import os
import random
import discord

from discord.ext import commands
from dotenv import load_dotenv
from dice_pool import DicePool, DicePoolState
from die import Die, DieType

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='/')


@bot.command(name='v', help='Simulates rolling vtm dice.')
async def roll(ctx, number_of_dice: int, number_of_hunger: int):
    dice_pool = DicePool()
    dice_pool.roll(number_of_dice, number_of_hunger)
    dice_text = getDiceAsText(dice_pool.results)
    dice_shapes = getDiceAsEmotes(dice_pool.results)
    title = f'{dice_pool.Successes()} successes'

    await send_message(ctx, title, dice_text, dice_shapes, dice_pool.state, getMessageColor(dice_pool.state))


def getMessageColor(state):
    if (state == DicePoolState.BEASTIAL):
        return 0xFF0000  # Red
    if (state == DicePoolState.FAILURE):
        return 0xFF6600  # Orange
    if (state == DicePoolState.SUCCESS):
        return 0x00FF00  # Green
    if (state == DicePoolState.CRITICAL):
        return 0xFFFF00  # Yellow
    if (state == DicePoolState.MESSY):
        return 0x6600FF  # Purple

    return 0xFFFFFF  # Black


def getDiceAsText(dice: list):
    result = []
    for die in dice:
        if (die.die_value < 6):
            result.append(f'~~{die.die_value}~~')
        else:
            result.append(f'{die.die_value}')
    return ','.join(result)


def getDiceAsEmotes(dice: list):
    result = []
    for die in dice:
        shape = 'square' if die.die_type == DieType.HUNGER else 'circle'
        if die.die_value == 1:
            result.append(f':red_{shape}:')
        elif die.die_value >= 2 and die.die_value <= 5:
            result.append(f':orange_{shape}:')
        elif die.die_value >= 6 and die.die_value <= 9:
            result.append(f':green_{shape}:')
        elif die.die_value == 10:
            result.append(f':blue_{shape}:')
    return ','.join(result)


async def send_message(ctx, title, dice_text, dice_shapes, state, state_color):
    embedVar = discord.Embed(
        title=title, description=dice_shapes, color=state_color)
    embedVar.add_field(name=state.name, value=dice_text)
    await ctx.send(embed=embedVar)


bot.run(TOKEN)
