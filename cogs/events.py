

## Built-in modules:

## Pip modules:
## Framework:
from disnake.ext.commands import Cog, Bot
from disnake.ext.tasks import loop
from disnake import AppCommandInteraction
from disnake.ext.commands import Context
from disnake.ext.commands.errors import CommandNotFound, MissingPermissions, \
    UserInputError, NoPrivateMessage, NotOwner, CommandInvokeError
from disnake.errors import InteractionResponded, InteractionTimedOut


## Bot modules:
from config import COMMAND_PREFIX, BOT_NAME
from bot_modules.bot_logger import on_ready_logger, cog_init_logger, error_logger
from bot_modules.emoji import STOP_SIGN_EM
from bot_modules.exceptions.balance_exceptions import ZeroBalanceError, \
    NegativeBalanceError

class Events(Cog):
    """Events cog for bot.

    Args:
        Cog (class): Cog class.
    """
    def __init__(
        self,
        bot: Bot
    ) -> None:
        self.bot: Bot = bot
    
    
    @Cog.listener(name="on_ready")
    async def on_ready(self) -> None:
        """
        Event when bot is ready.
        """
        on_ready_logger()


    ## Calls on error in command.
    @Cog.listener("on_command_error")
    async def on_command_error(
        self,
        ctx: Context,
        error: Exception
    ) -> None:
        """Handler of the command errors.

        Args:
            error (Exception)
        """
        author_mention: str = ctx.author.mention
        
        if isinstance(error, CommandNotFound):
            await ctx.send(
                content=f"""
{STOP_SIGN_EM} Уважаемый {author_mention}, такой команды `не существует!`
"""
            )
        elif isinstance(error, MissingPermissions | NotOwner):
            await ctx.send(
                content=f"""
{STOP_SIGN_EM} Уважаемый {author_mention}, у вас \
`недостаточно прав` для исполнения команды \"*{ctx.command.name}*\"!
"""
            )
        elif isinstance(error, UserInputError):
            await ctx.send(
                content=f"""
{STOP_SIGN_EM} Уважаемый {author_mention}, вы передали \
`неверные аргументы` при использовании команды \"*{ctx.command.name}*\"!\
Правильное использование: \"*{ctx.command.brief}*\"
"""
            )
        else:
            await ctx.send(
                content=f"""
"{STOP_SIGN_EM} Уважаемый {author_mention}, при использовании \
команды \"*{ctx.command.name}*\" `произошла ошибка`: {error}
"""
            )
            error_logger(
                error=error
            )


    ## Calls on error in slash_command.
    @Cog.listener("on_slash_command_error")
    async def on_slash_command_error(
        self,
        inter: AppCommandInteraction,
        error: Exception
    ) -> None:
        """Errors handler in slash_commands

        Args:
            inter (AppCommandInteraction)
            error (Exception)
        """
        author_mention: str = inter.author.mention
        
        if isinstance(error, NoPrivateMessage):
            await inter.send(f"""
{STOP_SIGN_EM} Уважаемый {author_mention},
вы не можете использовать эту команду в `личных сообщениях!`
""",
                ephemeral=True
            )
        elif isinstance(error, InteractionResponded):
            await inter.send(f"""
{STOP_SIGN_EM} Уважаемый {author_mention},
при исполнении команды `произошла ошибка!`
""",
                ephemeral=True
            )
        elif isinstance(error, InteractionTimedOut):
            await inter.send(f"""
{STOP_SIGN_EM} Уважаемый {author_mention}, `время ожидания вышло!`
""",
                ephemeral=True
            )
        elif isinstance(error, CommandInvokeError):
            original_error: Exception = error.original
            
            if isinstance(original_error, NegativeBalanceError):
                await inter.send(f"""
{STOP_SIGN_EM} Уважаемый {author_mention}, `нельзя добавлять отрицательный баланс!`
""",
                    ephemeral=True
                )
            elif isinstance(original_error, ZeroBalanceError):
                await inter.send(f"""
{STOP_SIGN_EM} Уважаемый {author_mention}, `нельзя добавлять нулевой баланс!`
ГЕНИАЛЬНО
""",
                    ephemeral=True
                )
        else:
            await inter.send(
                content=f"""
{STOP_SIGN_EM} Уважаемый {author_mention}, при использовании \
команды `произошла ошибка`: {error}
""",
                ephemeral=True
            )
            error_logger(
                error=error
            )


def setup(bot: Bot) -> None:
    bot.add_cog(Events(bot=bot))
    cog_init_logger(cog_name="Events")