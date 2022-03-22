# Taken from https://github.com/unl1k3ly/AnchorHODL/blob/58dd0ba5ee5cac5bc355520e8705cb805d6f9bc9/logging_config.py
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(message)s",
            # 'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            "datefmt": "%d-%m-%Y %H:%M:%S",
        },
        "info_logger_format": {"format": "%(asctime)s %(message)s", "datefmt": "%d-%m-%Y %H:%M:%S",},
        "colored": {
            "()": "colorlog.ColoredFormatter",
            # 'format': "%(asctime)s - %(name)s: %(log_color)s%(levelname)-4s%(reset)s %(blue)s%(message)s",
            "format": "%(asctime)s - %(log_color)s%(levelname)-4s%(reset)s %(blue)s%(message)s",
            "datefmt": "%d-%m-%Y %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/info.log",
            "maxBytes": 1024 * 1024 * 5,  # 5MB
            "backupCount": 5,
            "formatter": "standard",
        },
        "debug_console_handler": {
            "level": "DEBUG",
            "formatter": "colored",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "arbstrat": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/arbstrat.log",
            "maxBytes": 1024 * 1024 * 5,  # 5MB
            "backupCount": 5,
            "formatter": "info_logger_format",
        },
        "werkzeug": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/werkzeug.log",
            "maxBytes": 1024 * 1024 * 5,  # 5MB
            "backupCount": 5,
        },
    },
    "loggers": {
        "": {"handlers": ["default", "debug_console_handler"], "level": "INFO", "propagate": True,},
        "arbstrat": {"handlers": ["arbstrat"], "level": "INFO", "propagate": False,},
        "werkzeug": {"handlers": ["werkzeug"], "level": "INFO", "propagate": False,},
        "urllib3.connectionpool": {"level": "WARNING",},
    },
}
