import json
import logging.config
from pathlib import Path

logger = logging.getLogger(__name__)


def setup_logging():
    config_file = Path(".logging_configs/base_config.json")
    with open(config_file, 'r') as file:
        config = json.load(file)
    logging.config.dictConfig(config)


def main():
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
