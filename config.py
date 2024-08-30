
## Built-in modules:
from os import getenv
from os import PathLike
from os.path import dirname

## Pip modules:
from dotenv import load_dotenv
## Framework:
from disnake.activity import Game

## Load environment
load_dotenv()

## Get bot token.
TOKEN: str = getenv("TOKEN")

## Other bot options:
COMMAND_PREFIX: str = "$"
DESCRIPTION: str = """
Тестовый бот для изучения работы с MySQL.
"""
OWNER_ID: int = 1250875663108538555
ACTIVITY: Game = Game(
    name="MySQL.",
    platform="Gachimuchi"
)
DIR_PATH: PathLike = dirname(__file__)
BOT_NAME: str = "BaseBOT"

## Database options.
DB_PASSWORD: str = getenv("DB_PASSWORD")
DB_PORT: int = int(getenv("DB_PORT"))
DB_HOST: str = getenv("DB_HOST")
DB_NAME: str = getenv("DB_NAME")
DB_USER: str = getenv("DB_USER")