import logging
import sys
import os


def setup_logging():
    os.makedirs('logs', exist_ok=True)
    file_handler = logging.FileHandler(
        filename='logs/app.log',
        encoding='utf-8',
        mode='a'
    )
    file_handler.setLevel(logging.DEBUG)

    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    stdout_handler.addFilter(lambda record: record.levelno < logging.ERROR)

    stderr_handler = logging.StreamHandler(stream=sys.stderr)
    stderr_handler.setLevel(logging.ERROR)

    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        datefmt='%d.%m.%Y %H:%M',
        handlers=[file_handler, stdout_handler, stderr_handler]
    )

