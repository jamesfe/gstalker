# -*- coding: utf-8 -*-


from database import engine
from models import BASE
from utils import load_config


def main():
    config = load_config('./config/config.json')
    db_config = config.get('db')
    eng = engine(db_config)
    print('deleting all')
    BASE.metadata.drop_all(eng)
    print('creating all')
    BASE.metadata.create_all(eng)


if __name__ == '__main__':
    main()
