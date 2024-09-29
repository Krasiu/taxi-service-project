import inspect
import logging
import sys

from loguru import logger

from common.schemas import Coordinates


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def configure_logging(log_level: str = "INFO", *, serialize: bool = False) -> None:
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    logger.remove(0)
    logger.add(sys.stdout, level=log_level, serialize=serialize)


def calculate_manhattan_distance(coordinates1: Coordinates, coordinates2: Coordinates) -> int:
    return abs(coordinates1.x - coordinates2.x) + abs(coordinates1.y - coordinates2.y)
