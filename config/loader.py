import os

def load_config():
    from config import base, dev, prod
    env = os.getenv('APP_ENV', 'dev').lower()

    if env == 'prod':
        return prod
    elif env == 'dev':
        return dev
    else:
        return base