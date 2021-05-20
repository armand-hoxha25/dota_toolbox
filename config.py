import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG=True
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    MONGO_DB_URI = os.environ.get(
        "DATABASE_URL"
    )
