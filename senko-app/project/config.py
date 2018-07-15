"""
システム・DB設定ファイル
"""
import os

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8'.format(**{
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', 'password'),
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('DB_DATABASE', 'senko'),
    })
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('DB_SECRET_KEY', 'some-secret-string')
    SQLALCHEMY_ECHO = True

Config = DevelopmentConfig
