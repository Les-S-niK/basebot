
## Built-in modules:
from typing import Union
## Pip modules:
from pymysql.cursors import DictCursor
from pymysql import connect, Connection

## Bot modules
from config import  DB_PORT, DB_HOST, DB_NAME, DB_PASSWORD, \
    DB_USER
from bot_modules.bot_logger import error_logger

try:
    ## Connect to database.
    connection: Connection = connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        password=DB_PASSWORD,
        user=DB_USER,
        cursorclass=DictCursor
    )
    
except Exception as error:
    error_logger(error=error)


class UserBalanceManager(object):
    """A manager class of users balance.

    Args:
        object (class): basic inheritance class.
    """
    def __init__(
        self,
        user_id: int,
        username: str,
        money_count: float = 0.0
    ) -> None:
        """Initialization the UserBalanceManager class. 
        Add .self vars.

        Args:
            user_id (int): user id.
            username (str): username.
            money_count (float): old user balance.
        """
        self.USER_ID: int = user_id
        self.USERNAME: str = username
        self.MONEY_COUNT: float = money_count
        self.old_balance: Union[float, bool]  = self._get_old_user_balance()


    def _get_old_user_balance(self) -> Union[float, bool]:
        """Get old user balance.

        Returns:
            float: old user balance.
        """
        ## Create a cursor instance.
        with connection.cursor(DictCursor) as mysql_cursor:
            GET_SQL_QUERY: str = f"SELECT balance FROM users_info WHERE id = {self.USER_ID};"
            ## Get information from DB.
            mysql_cursor.execute(GET_SQL_QUERY)
            fetched_info: list = mysql_cursor.fetchone()
            ## Check if info is not null.
            if fetched_info is None:
                return None
            else:
                old_balance: float = fetched_info.get("balance")
                return float(old_balance)


    def manage_user_balance(
        self,
        add_money: bool
    ) -> float:
        """Add or Sub money to old user balance.

        Args:
            add_money (bool): Add money or Sub. If True - add, else - sub.
        
        Returns:
            float: new user balance.
        """

        ## Do some operations with balance and MONEY_COUNT.
        if self.old_balance is not None:
            old_balance: float = self.old_balance
        else:
            old_balance: float = 0.0
        
        new_balance: float = old_balance + self.MONEY_COUNT if add_money \
            else old_balance - self.MONEY_COUNT
        ## If user not in db - add him, else - update his info.
        if self.old_balance is None:
            SQL_QUERY: str = f"""
            INSERT INTO users_info (id, name, balance)
            VALUES ({self.USER_ID}, "{self.USERNAME}", {new_balance});
            """
        else:
            SQL_QUERY: str = f"""
            UPDATE users_info
            SET balance = {new_balance}
            WHERE id = {self.USER_ID};
            """
        
        with connection.cursor(DictCursor) as mysql_cursor:
            ## Executing SQL query.
            mysql_cursor.execute(SQL_QUERY)
            ## Commiting database.
            connection.commit()
        
        return new_balance