# -*- coding: utf-8 -*-

from copy import copy

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy_utils import database_exists, create_database


def engine(config):
    url = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}'
    engine = create_engine(url.format(**config), pool_size=1)
    if not database_exists(engine.url):
        try:
            temp_config = copy(config)
            temp_config['user'] = config.get('user', 'postgres')
            temp_config['password'] = config.get('password', 'postgres')
            temp_engine = create_engine(url.format(**temp_config), pool_size=1)
            create_database(temp_engine.url)
        except IntegrityError:
            return engine  # db has already been created
    return engine
