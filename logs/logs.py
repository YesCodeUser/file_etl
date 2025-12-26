import logging
import sys
import os
from config import LOG_FILE, LOG_LEVEL, LOG_DIR


def setup_logging():
    os.makedirs(LOG_DIR, exist_ok=True)
    file_handler = logging.FileHandler(
        filename=LOG_FILE,
        encoding='utf-8',
        mode='a'
    )
    file_handler.setLevel(logging.DEBUG)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    stdout_handler.addFilter(lambda record: record.levelno < logging.ERROR)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR)

    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        datefmt='%d.%m.%Y %H:%M',
        handlers=[file_handler, stdout_handler, stderr_handler]
    )

