# coding: utf-8
"""
"""

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:dev@mysql/lesson1?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = False
REDIS_URL = 'redis://{}:{}/0'.format('172.18.0.2', 6379)
