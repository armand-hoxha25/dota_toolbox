import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    MONGO_DB_URI = "mongodb+srv://{}:{}@dota-toolbox-east.1gro0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"\
        .format(os.environ.get("MONGO_USER"), os.environ.get("MONGO_PASSWORD"))
