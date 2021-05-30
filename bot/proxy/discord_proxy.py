from discord.ext.commands import Context
from common.utils import string_to_numbers


class PoolCommandResult():

    def __init__(self) -> None:
        self.message_id = None
        self.author_name = ""
        self.regular_dice = list()
        self.hunger_dice = list()


class DiscordProxy():

    async def get_last_pool_command(self, ctx: Context) -> PoolCommandResult:
        message_command = None
        message_result = None

        botId = ctx.bot.user.id
        authorId = ctx.author.id
        pool_command_result = PoolCommandResult()

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
            return pool_command_result

        pool_command_result.message_id = message_command.id
        pool_command_result.author_name = message_command.author.name
        if message_result.embeds and len(message_result.embeds) > 0:
            message_embed = message_result.embeds[0]
            for field in message_embed.fields:
                if field.name == 'regular':
                    pool_command_result.regular_dice = \
                        pool_command_result.regular_dice + \
                        string_to_numbers(field.value)
                    continue

                if field.name == 'hunger':
                    pool_command_result.hunger_dice = \
                        pool_command_result.hunger_dice + \
                        string_to_numbers(field.value)
                    continue

        return pool_command_result
