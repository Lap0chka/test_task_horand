import logging
import os

import colorlog

from .base import BASE_DIR

LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

color_formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
)

stream_handler = colorlog.StreamHandler()
stream_handler.setLevel("DEBUG")
stream_handler.setFormatter(color_formatter)

root_logger = logging.getLogger()
root_logger.setLevel("DEBUG")
root_logger.addHandler(stream_handler)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "file": {
            "format": "[{asctime}] {levelname} {module} | {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, "events.log"),
            "formatter": "file",
            "level": "INFO",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True,
        },
        "event_logger": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
