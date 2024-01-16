import logging


def setup_logging(logger_name: str) -> logging.Logger:
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(logger_name)
