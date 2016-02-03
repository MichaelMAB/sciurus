import os

CONFIG = os.getenv('CONFIG', 'production')


def make_uri(db):
    return 'mongodb://{user}:{pswd}@{host}:{port}/{db}'.format(
        user=db['USER'],
        pswd=db['PASSWORD'],
        host=db['HOST'],
        port=db['PORT'],
        db=db['DB']
    )


class Config:
    DEFAULT = 'test'


class TestConfig(Config):

    HOST = 'localhost'
    DB = 'test'


class ProductionConfig(Config):

    mongo_db = {}
    mongo_db['HOST'] = os.getenv('PRODUCTION_HOST', 'localhost')
    mongo_db['USER'] = os.getenv('PRODUCTION_USER', 'localhost')
    mongo_db['PASSWORD'] = os.getenv('PRODUCTION_PASSWORD', 'localhost')
    mongo_db['PORT'] = str(os.getenv('PRODUCTION_PORT', 'localhost'))
    mongo_db['DB'] = os.getenv('PRODUCTION_DB', 'localhost')
    HOST = make_uri(mongo_db),
    DB = mongo_db['DB']

configs = {
    'production': ProductionConfig(),
    'testing': TestConfig(),
    'default': TestConfig()
}
