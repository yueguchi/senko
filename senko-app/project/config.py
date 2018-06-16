"""
システム・DB設定ファイル
"""
import os

class DevelopmentConfig:
    # Flask
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/flask_sample?charset=utf8'.format(**{
    #     'user': os.getenv('DB_USER', 'root'),
    #     'password': os.getenv('DB_PASSWORD', ''),
    #     'host': os.getenv('DB_HOST', 'localhost'),
    # })
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'some-secret-string'
Config = DevelopmentConfig