
## Pip modules:
## Framework modules:
from disnake.ext.commands import Bot
from disnake import Intents

## Bot modules:
from config import TOKEN, COMMAND_PREFIX, DESCRIPTION, \
    OWNER_ID, ACTIVITY
from bot_modules.bot_logger import start_logger, error_logger


## Create a bot instance.
bot: Bot = Bot(
    command_prefix=COMMAND_PREFIX,
    help_command=None,
    description=DESCRIPTION,
    owner_id=OWNER_ID,
    intents=Intents.all(),
    activity=ACTIVITY
)
## Load all the bot extentions.
bot.load_extensions("cogs/")

try:
    start_logger()
    ## Turn on the bot.
    bot.run(
        token=TOKEN
    )
except Exception as error:
    error_logger(
        error=error
    )