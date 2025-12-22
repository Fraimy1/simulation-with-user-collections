from typing import NoReturn
from loguru import logger  # type: ignore[import-not-found]
from casino_lab4.core.errors import CustomError

def log_and_raise(error: CustomError) -> NoReturn:
    logger.error(f"{error.__class__.__name__}: {error.message}")
    raise error
