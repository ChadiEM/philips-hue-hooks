import logging.config

logging_config = dict(
    version=1,
    disable_existing_loggers=False,
    formatters={
        'f': {'format':
                  '[%(asctime)s] %(levelname)s - %(message)s'}
    },
    handlers={
        'h': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'stream': 'ext://sys.stdout',
              'level': logging.INFO}
    },
    root={
        'handlers': ['h'],
        'level': logging.INFO
    }
)

logging.config.dictConfig(logging_config)
