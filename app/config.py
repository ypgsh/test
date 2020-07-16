
import os
import logging

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

class Config:
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WORK_ROOT = os.environ.get('WORK_ROOT', '/workroot')
    JWT_SECRET_KEY = 'se-simright-valve'
    JWT_TOKEN_NAME= 'simright_token'

    MAIN_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    DATABASE_ADDR = os.environ.get('DATABASE_ADDR') or 'localhost:5437'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres_rotor@{}/postgres'.format(DATABASE_ADDR)

    DATA_DIR = os.path.join(MAIN_DIR, 'data')
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)

    LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', None)
    if not LOGGING_LEVEL or LOGGING_LEVEL not in ('fatal', 'error', 'debug'):
        LOGGING_LEVEL = logging.ERROR
    else:
        LOGGING_LEVEL = {
            'fatal': logging.FATAL,
            'error': logging.ERROR,
            'debug': logging.DEBUG} \
            .get(LOGGING_LEVEL)

    logging.basicConfig(
        level=logging.ERROR,
        format="%(asctime)s %(pathname)s[line:%(lineno)d] %(levelname)s %(message)s",
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename=os.path.join(DATA_DIR, 'controller.log'),
        filemode='a'
    )


class DevelopmentConfig(Config):
    # 屏幕输出
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s %(pathname)s[line:%(lineno)d] %(levelname)s %(message)s")
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO=True


    # def __new__(cls, *args, **kwargs):
    #     print(cls.__name__[:-6])
    #     return object.__new__(cls, *args, **kwargs)


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres_rotor@{}/postgres_test'.format(Config.DATABASE_ADDR)
    WORK_ROOT = '/workroot/test'

class ProductConfig(Config):
    DEBUG = False
    TESTING = True

    SENTRY_CLIENT_DNS_KEY = os.environ.get('SENTRY_CLIENT_DNS_KEY') or None
    if SENTRY_CLIENT_DNS_KEY:
        sentry_logging = LoggingIntegration(
            level=logging.INFO,  # Capture info and above as breadcrumbs
            event_level=logging.DEBUG  # Send errors as events
        )
        sentry_sdk.init(
            dsn=SENTRY_CLIENT_DNS_KEY,
            integrations=[sentry_logging]
        )


def get_config(config_name = None):
    config_dict=dict(test=TestConfig,
                     product=ProductConfig,
                     develop=DevelopmentConfig)
    return config_dict.get(config_name, ProductConfig)()
