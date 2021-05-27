# bot.py
import os
import discord
import typing
import logging

from discord.utils import get
from discord.message import Message

from discord.ext import commands
from discord.ext.commands import Context, Bot

from dotenv import load_dotenv

from command_result import CommandResult, CommandResultState
from pool_command import PoolCommand
import colours as Colours

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
logging.basicConfig(level=logging.ERROR)
logging.info(discord.version_info)

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


@bot.command(name='will', help='Use willpower to reroll up to 3 failed regular dice')
async def will(ctx: Context):
    botId = ctx.bot.user.id
    authorId = ctx.author.id

    message_command = None
    message_result = None
    messages = await ctx.channel.history().flatten()
    for message in messages:
        if message.author.id != botId or len(message.embeds) <= 0 or message.reference is None:
            continue

        message_ref = await ctx.fetch_message(message.reference.message_id)
        if (
            message_ref is None or
            not message_ref.content.startswith('/pool') or
            message_ref.author.id != authorId
        ):
            continue

        message_command = message_ref
        message_result = message
        break

    if not message_command or not message_result:
        return

    embed = discord.Embed(title='Previous Roll')
    embed.add_field(
        name='content', value=f'{message_result.content}', inline=False)
    if message_result.embeds and len(message_result.embeds) > 0:
        message_embed = message_result.embeds[0]
        embed.add_field(
            name='title', value=f'{message_embed.title}', inline=False)
        for field in message_embed.fields:
            embed.add_field(name=f'{field.name}', value=f'{field.value}')

    await ctx.send(
        content=f'{message_command.author.name} makes a willpower roll',
        embed=embed,
        reference=ctx.message)


@bot.event
async def on_command_error(ctx, error):
    raise error


def getEmoji(emoji_name: str):
    return discord.utils.get(bot.emojis, name=emoji_name)


async def send_message(ctx, message):
    content = ''
    if message["dice_emojis"]:
        content = message["dice_emojis"]

    embedVar = discord.Embed(
        title=f'{message["state"]}, {message["title"]}', color=message["colour"])
    if message["regular_dice_text"]:
        embedVar.add_field(
            name="regular", value=f'{message["regular_dice_text"]}')
    if message["hunger_dice_text"]:
        embedVar.add_field(
            name="hunger", value=f'{message["hunger_dice_text"]}')

    if content:
        await ctx.send(content=content, embed=embedVar, reference=ctx.message)
    else:
        await ctx.send(embed=embedVar, reference=ctx.message)


async def send_error(ctx, message):
    embedVar = discord.Embed(
        title=f'{message}', color=Colours.RED)
    embedVar.add_field(
        name='Usage', value='/pool [pool dice] [hunger dice]', inline=False)
    embedVar.add_field(name='Example', value='/pool 10 3', inline=False)

    await ctx.send(embed=embedVar)


bot.run(TOKEN)
