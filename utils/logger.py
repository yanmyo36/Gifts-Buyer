import datetime
import logging
import sys

SUCCESS_LEVEL = 25
logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")


class SimpleFormatter(logging.Formatter):
    def format(self, record):
        timestamp = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")
        formatted_levelname = f"[{timestamp}] -  [{record.levelname}] -"
        record.levelname = formatted_levelname
        return super().format(record)


class CustomLogger(logging.Logger):
    def success(self, msg, *args, **kwargs):
        if self.isEnabledFor(SUCCESS_LEVEL):
            self._log(SUCCESS_LEVEL, msg, args, **kwargs)


logging.setLoggerClass(CustomLogger)

logger = logging.getLogger("gifts_buyer")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

formatter = SimpleFormatter('%(levelname)s %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


def info(message: str) -> None:
    logger.info(message)


def warn(message: str) -> None:
    logger.warning(message)


def error(message: str) -> None:
    logger.error(message)


def success(message: str) -> None:
    if isinstance(logger, CustomLogger):
        logger.success(message)
    else:
        logger.info(f"[SUCCESS] {message}")


def log_same_line(message: str, level: str = "INFO") -> None:
    timestamp = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")
    formatted_message = f"\r[{timestamp}] -  [{level.upper()}] - {message}"
    print(formatted_message, end="\r", flush=True)
