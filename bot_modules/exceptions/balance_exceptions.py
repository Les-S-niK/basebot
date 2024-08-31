
## Built-in modules:
from typing import Any


class ZeroBalanceError(Exception):
    """Raises when you try to add a null balance.

    Args:
        Exception (class): base exceptions class.
    
    """
    def __call__(
        self,
        message: str = None,
        *args: Any,
        **kwds: Any
    ) -> None:
        """Call the Exception.

        Args:
            message (str): message to send. Optional.

        """
        return super().__call__(
            message,
            args,
            kwds
        )


class NegativeBalanceError(Exception):
    """Raises when you try to add a substract balance,
    where it not supported.

    Args:
        Exception (class): base exceptions class.
    
    """
    def __call__(
        self,
        message: str = None,
        *args: Any,
        **kwds: Any
    ) -> None:
        """Call the Exception.

        Args:
            message (str): message to send. Optional.

        """
        return super().__call__(
            message,
            args,
            kwds
        )