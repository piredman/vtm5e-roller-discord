# bot.py
import os
import discord

from discord.utils import get
from discord.ext import commands
from discord.ext.commands import Context, Bot

from dotenv import load_dotenv

from command_result import CommandResult, CommandResultState
from roll_command import RollCommand
import colours as Colours

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='/')


@bot.command(name='pool', help='Simulates rolling vtm dice pool')
async def roll(ctx: Context, pool_dice: int, hunger_dice: int):
    command = RollCommand(getEmoji)
    result = command.roll(pool_dice, hunger_dice)
    if (result.state == CommandResultState.SUCCESS):
        await send_message(ctx, result.payload)
    else:
        await send_error(ctx, result.payload)


@bot.event
async def on_command_error(ctx, error):
    await send_error(ctx, f'{error}')
    raise error


def getEmoji(emoji_name: str):
    return discord.utils.get(bot.emojis, name=emoji_name)


async def send_message(ctx, message):
    embedVar = discord.Embed(
        title=f'{message["state"]}, {message["title"]}', description=message["dice_text"], color=message["colour"])

    await ctx.send(message["dice_emojis"])
    await ctx.send(embed=embedVar)


async def send_error(ctx, message):
    embedVar = discord.Embed(
        title=f'Sorry, please try again', color=Colours.RED)
    embedVar.add_field(
        name='Usage', value='/pool [pool dice] [hunger dice]', inline=False)
    embedVar.add_field(name='Example', value='/pool 10 3', inline=False)

    await ctx.send(embed=embedVar)


bot.run(TOKEN)
