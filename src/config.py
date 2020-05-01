# config.py
import os

class Config:
    DEBUG = False
    TESTING = False

    POSTGRES = {
        'user': os.environ['POSTGRES_USER'],
        'pw': os.environ['POSTGRES_PASSWORD'] ,
        'db': os.environ['POSTGRES_DB'],
        'host': 'postgres',
        'port': '5432'
    }

    APP_NAME = os.environ['APP_NAME']

    GITHUB_PROJECT = os.environ['GITHUB_PROJECT']
    GITHUB_TOKEN = os.environ['GITHUB_TOKEN']

class ProductionConfig(Config):
    LOG_LEVEL = 'DEBUG'

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class TestingConfig(Config):
    TESTING = True
    LOG_LEVEL = 'DEBUG'
