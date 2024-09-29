import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'qwe123'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tamanager.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    