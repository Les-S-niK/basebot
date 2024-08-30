
## Pip modules:
from loguru import logger

## Bot modules:
from config import DIR_PATH, BOT_NAME


logger.add(
    sink=f"{DIR_PATH}/logs.log",
    level="DEBUG",
    rotation="1 MB",
    compression="zip"
)

def start_logger() -> None:
    """
    Logger for bot start.
    """
    logger.info(
        f"""
        Bot <<{BOT_NAME}>> on startup now.
        """
    )


def on_ready_logger() -> None:
    """
    Logger when bot turn on.
    """
    logger.info(
        f"""
        Bot <<{BOT_NAME}>> is ready!.
        """
    )


def cog_init_logger(
    cog_name: str
) -> None:
    """Logger of the cog initialization. 

    Args:
        cog_name (str): Cog name.
    """
    logger.info(
        f"""
        Cog <<{cog_name}>> initialization
        """
    )


def error_logger(
    error: Exception
) -> None:
    """Logger of the errors.

    Args:
        error (Exception): An occured error.
    """
    logger.error(
        f"""
        An error occured while running the {BOT_NAME}
        <<<{error}>>>
        """
    )


def command_logger(
    command_name: str,
    user_name: str,
    channel_name: str,
    guild_name: str,
    command_args: str,
    *args
) -> None:
    """Commands logger.

    Args:
        command_name (str): command name.
        user_name (str): user name.
        channel_name (str): channel name.
        guild_name (str): guild name.
        command_args (str): command arguments.
    """
    logger.debug(
        f"""
        <<<{BOT_NAME}>>>
        Command name: {command_name},
        User name: {user_name},
        Channel name: {channel_name},
        Guild name: {guild_name}
        Command args: 
        {command_args},
        {args}
        """
    )

