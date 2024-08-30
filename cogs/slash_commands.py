
## Built-in modules:

## Pip modules:
from datetime import datetime
## Framework:
from disnake.ext.commands import Cog, Bot
from disnake.ext.commands import slash_command
from disnake import AppCommandInteraction
from disnake import Embed, Color

## Bot modules:
from config import COMMAND_PREFIX, BOT_NAME
from bot_modules.emoji import ROBOT_EM, VICTORY_HAND_EM
from bot_modules.bot_logger import command_logger, cog_init_logger
from bot_modules.sql_requests import UserBalanceManager
from bot_modules.parsers.proxies_parser import ProxiesParser


class SlashCommands(Cog):
    """SlashCommands cog for bot.

    Args:
        Cog (class): Cog class.
    """
    def __init__(
        self,
        bot: Bot
    ) -> None:
        self.bot: Bot = bot


    @slash_command(
        name="balance",
        description=f"Нужен ваш баланс? Можете узнать его тут! {ROBOT_EM}"
    )
    async def balance(
        self,
        inter: AppCommandInteraction
    ) -> None:
        """Checks the author balance.

        Args:
            inter (AppCommandInteraction)
        """
        balance_manager: UserBalanceManager = UserBalanceManager(
            user_id=inter.author.id,
            username=inter.author.name,
            money_count=None
        )
        user_balance: float = balance_manager.old_balance
        ## Check if user doesn't have any balance.
        if user_balance is None:
            user_balance: float = 0.0
        
        await inter.response.send_message(
            embed=Embed(
                title="**Баланс: **",
                timestamp=datetime.now(),
                color=Color.random()
            )
            .add_field(
                name=f"{inter.author.global_name}, ваш баланс:",
                value=f"**{user_balance}**"
            )
            .set_author(
                name=inter.author.global_name,
                icon_url=inter.author.avatar.url
            ),
            delete_after=30
        )
        return None


    @slash_command(
        name="get_proxies",
        description=f"Нужны прокси? Можете получить их тут! {ROBOT_EM}"
    )
    async def get_proxies(
        self, 
        inter: AppCommandInteraction,
        protocol: str,
        countries_to_ignore: str = None
    ) -> None:
        """Get proxies from API parser.

        Args:
            inter (AppCommandInteraction)
            protocol (str): proxy protocol.
            countries_to_ignore (str, optional). Defaults to None.
        """
        proxy_parser: ProxiesParser = ProxiesParser(
            protocol=protocol,
            countries_to_ignore=[countries_to_ignore]
        )
        proxies: list = proxy_parser.proxies
        
        await inter.response.send_message(
            embed=Embed(
                title="**Прокси: **",
                timestamp=datetime.now(),
                color=Color.random(),
                description=f"**{proxies}**"
            )
            .set_author(
                name=inter.author.global_name,
                icon_url=inter.author.avatar.url
            )
            .set_footer(
                text="Если возвращает NONE, попробуйте запустить команду заново."
            ),
            delete_after=30
        )
        return None



def setup(
    bot: Bot
) -> None:
    bot.add_cog(SlashCommands(bot=bot))
    cog_init_logger(cog_name="SlashCommands")