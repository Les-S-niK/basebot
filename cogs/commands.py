
## Built-in modules:

## Pip modules:
## Framework:
from disnake.ext.commands import Cog, Bot
from disnake.ext.commands import command, has_guild_permissions, is_owner
from disnake.ext.commands import Context

## Bot modules:
from config import COMMAND_PREFIX, BOT_NAME
from bot_modules.bot_logger import command_logger, cog_init_logger
from bot_modules.sql_requests import UserBalanceManager



class Commands(Cog):
    """Commands cog for bot.

    Args:
        Cog (class): Cog class.
    """
    def __init__(
        self,
        bot: Bot
    ) -> None:
        self.bot: Bot = bot


    @is_owner()
    @command(
        name="exit",
        description="Turn off the bot.",
        brief=f"{COMMAND_PREFIX}exit"
    )
    async def exit(
        self,
        ctx: Context
    ) -> None:
        """Exit command.

        Args:
            ctx (Context): Context object.
        """
        command_logger(
            command_name="exit",
            user_name=f"{ctx.author.name} ({ctx.author.global_name})",
            channel_name=ctx.channel.name,
            guild_name=ctx.guild.name,
            command_args=None
        )
        
        await ctx.send(
            content=f"{BOT_NAME} is now offline!"
        )
        exit()


def setup(
    bot: Bot
) -> None:
    bot.add_cog(Commands(bot=bot))
    cog_init_logger(cog_name="Commands")