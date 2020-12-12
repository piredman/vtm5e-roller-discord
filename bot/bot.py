# bot.py
import os
import discord

from discord.utils import get
from discord.ext import commands
from discord.ext.commands import Context, Bot

from dotenv import load_dotenv

from dice_pool import DicePool
from dice_pool_message import DicePoolMessage
import colours as Colours

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='/')


@bot.command(name='pool', help='Simulates rolling vtm dice pool')
async def roll(ctx: Context, number_of_dice: int, number_of_hunger: int):
    dice_pool = DicePool()
    dice_pool.roll(number_of_dice, number_of_hunger)

    dice_pool_message = DicePoolMessage(dice_pool)
    message = dice_pool_message.formatMessage(getEmoji)

    await send_message(ctx, message)


@bot.event
async def on_command_error(ctx, error):
    embedVar = discord.Embed(
        title=f'Oh no, is that the sunrise peaking over the horizon?',
        color=Colours.RED)
    embedVar.add_field(
        name='Usage', value='/pool [pool dice] [hunger dice]', inline=False)
    embedVar.add_field(name='Example', value='/pool 10 3', inline=False)

    await ctx.send(embed=embedVar)
    raise error


def getEmoji(emoji_name: str):
    return discord.utils.get(bot.emojis, name=emoji_name)


async def send_message(ctx, message):
    embedVar = discord.Embed(
        title=f'{message["state"]}, {message["title"]}', description=message["dice_text"], color=message["colour"])

    await ctx.send(message["dice_emojis"])
    await ctx.send(embed=embedVar)


bot.run(TOKEN)
