# bot.py
import os
import random
import discord

from discord.utils import get
from discord.ext import commands
from discord.ext.commands import Context, Bot
from dotenv import load_dotenv
from dice_pool import DicePool, DicePoolState
from die import Die, DieType

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='/')


@bot.command(name='v', help='Simulates rolling vtm dice.')
async def roll(ctx: Context, number_of_dice: int, number_of_hunger: int):
    dice_pool = DicePool()
    dice_pool.roll(number_of_dice, number_of_hunger)
    dice_text = getDiceAsText(dice_pool.results)
    dice_shapes = getDiceAsEmotes(ctx, dice_pool.results)
    title = f'{dice_pool.Successes()} successes'

    await send_message(ctx, title, dice_text, dice_shapes, dice_pool.state, getMessageColor(dice_pool.state))


def getMessageColor(state):
    if (state == DicePoolState.BEASTIAL or state == DicePoolState.FAILURE):
        return 0xFF0000  # Red
    if (state == DicePoolState.CRITICAL or state == DicePoolState.MESSY):
        return 0x6600FF  # Purple
    return 0x00FF00  # Green


def getDiceAsText(dice: list):
    result = []
    for die in dice:
        die_text = f'~~{die.die_value}~~' if die.die_value < 6 else f'{die.die_value}'
        result.append(die_text)

    return ','.join(result)


def getDiceAsEmotes(ctx: Context, dice: list):
    result = []
    for die in dice:
        die_emote = ''
        if die.die_type == DieType.HUNGER:
            if die.die_value == 1:
                die_emote = discord.utils.get(
                    bot.emojis, name='hungerbeastial')
            elif die.die_value >= 2 and die.die_value <= 5:
                die_emote = discord.utils.get(
                    bot.emojis, name='hungerfailure')
            elif die.die_value >= 6 and die.die_value <= 9:
                die_emote = discord.utils.get(
                    bot.emojis, name='hungersuccess')
            elif die.die_value == 10:
                die_emote = discord.utils.get(
                    bot.emojis, name='hungercritical')
        else:
            if die.die_value >= 1 and die.die_value <= 5:
                die_emote = discord.utils.get(
                    bot.emojis, name='regularfailure')
            elif die.die_value >= 6 and die.die_value <= 9:
                die_emote = discord.utils.get(
                    bot.emojis, name='regularsuccess')
            elif die.die_value == 10:
                die_emote = discord.utils.get(
                    bot.emojis, name='regularcritical')
        result.append(str(die_emote))

    return ''.join(result)


async def send_message(ctx, title, dice_text, dice_shapes, state, state_color):
    embedVar = discord.Embed(
        title=f'{state.name}, {title}', description=dice_text, color=state_color)

    await ctx.send(dice_shapes)
    await ctx.send(embed=embedVar)


bot.run(TOKEN)
