import logging
from logging.config import dictConfig

LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)s | "
    "%(filename)s:%(lineno)d | %(message)s"
)

def setup_logging():
    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,

        "formatters": {
            "default": {
                "format": LOG_FORMAT,
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": "INFO",     # ← INFO и выше в консоль
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default",
                "filename": "app.log",
                "maxBytes": 5_000_000,
                "backupCount": 3,
                "encoding": "utf-8",
                "level": "DEBUG",    # ← DEBUG и выше в файл
            },
        },

        "root": {
            "level": "DEBUG",        # ← пропускаем всё
            "handlers": ["console", "file"],
        },
    })
