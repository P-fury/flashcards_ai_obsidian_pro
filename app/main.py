import atexit
import json
import logging.config
import os
import tomllib
from logging import Handler
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


# JSON CONFIG
# def setup_logging():
#     config_file = Path(".logging_configs/base_config.json")
#     with open(config_file, 'r') as file:
#         config = json.load(file)
#     logging.config.dictConfig(config)
#
#     queue_handler = logging.getHandlerByName("queue_handler")
#     if queue_handler is not None:
#         queue_handler.listener.start()
#         atexit.register(queue_handler.listener.stop)


def setup_logging() -> None:
    if os.getenv("TEST") == "1":
        return None
    config_file: Path = Path(".logging_configs/config.toml")
    with open(config_file, 'rb') as file:
        config: dict[str, Any] = tomllib.load(file)

    logging.config.dictConfig(config)

    queue_handler: Handler | None = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()  # type: ignore [attr-defined]
        atexit.register(queue_handler.listener.stop)  # type: ignore [attr-defined]


def main() -> None:
    setup_logging()
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")

    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("exception message")


if __name__ == "__main__":
    main()
