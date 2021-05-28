# bot.py
import os
import discord
import typing

from discord.utils import get
from discord.ext import commands
from discord.ext.commands import Context, Bot

from dotenv import load_dotenv

from command_result import CommandResult, CommandResultState
from pool_command import PoolCommand
import colours as Colours

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='/')


@bot.command(name='pool', help='Roll a dice pool of regular & hunger dice')
async def pool(ctx: Context, pool_dice: int, hunger_dice: typing.Optional[int]):
    command = PoolCommand(getEmoji)
    result = command.roll(pool_dice, hunger_dice)
    if (result.state == CommandResultState.SUCCESS):
        await send_message(ctx, result.payload)
    else:
        await send_error(ctx, result.payload)


@bot.command(name='rouse', help='Roll a rouse check, dice pool of 1 regular dice')
async def rouse(ctx: Context):
    command = PoolCommand(getEmoji)
    result = command.roll(number_of_dice=1, number_of_hunger=0)
    if (result.state == CommandResultState.SUCCESS):
        await send_message(ctx, result.payload)
    else:
        await send_error(ctx, result.payload)


@bot.event
async def on_command_error(ctx, error):
    raise error


def getEmoji(emoji_name: str):
    return discord.utils.get(bot.emojis, name=emoji_name)


async def send_message(ctx, message):
    embedVar = discord.Embed(
        title=f'{message["state"]}, {message["title"]}', color=message["colour"])

    embedVar.add_field(name="regular", value=f'{message["regular_dice_text"]}')
    if message["hunger_dice_text"]:
        embedVar.add_field(
            name="hunger", value=f'{message["hunger_dice_text"]}')

    emojis = message["dice_emojis"]
    if (emojis is not None):
        await ctx.send(message["dice_emojis"])

    await ctx.send(embed=embedVar)


async def send_error(ctx, message):
    embedVar = discord.Embed(
        title=f'{message}', color=Colours.RED)
    embedVar.add_field(
        name='Usage', value='/pool [pool dice] [hunger dice]', inline=False)
    embedVar.add_field(name='Example', value='/pool 10 3', inline=False)

    await ctx.send(embed=embedVar)


bot.run(TOKEN)
