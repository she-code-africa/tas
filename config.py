import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
TOP_LEVEL_DIR = os.path.abspath(os.curdir)


class Config(object):
    DEBUG = False
    TESTING = False


class Production(Config):
    DEBUG = False


class Development(Config):
    DEVELOPMENT = True
    DEBUG = True


class Testing(Config):
    TESTING = True


config = {
    'production': Production,
    'development': Development,
    'testing': Testing
}
