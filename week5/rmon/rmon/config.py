# coding=utf-8
""" rmon.config

rmon config file
"""

import os


class DevConfig(object):
    """development enviroment config
    """
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLAKCHEMY_DATABASE_URI = "sqlite://"
    TEMPLATES_AUTO_RELOAD = True


class ProductConfig(DevConfig):
    """product enviroment config
    """
    DEBUG = False

    # sqlite database file path
    path = os.path.join(os.getcwd(), "rmon.db").replace("\\", "/")
    SQLAKCHEMY_DATABASE_URI = "sqlite:///%s" % path
