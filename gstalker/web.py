# -*- coding: utf-8 -*-
"""Query the database for things."""

import logging
import sys

import coloredlogs
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
from sqlalchemy.orm import sessionmaker, scoped_session

from gstalker.database import engine
from gstalker.utils import load_config
from gstalker.handlers import (
    MainHandler,
    PackageHandler
    RecalculateFromExactHandler
)

logger = logging.getLogger('gstalker_server')
coloredlogs.install(format='%(asctime)s - %(levelname)s: %(message)s', level='DEBUG', logger=logger)
PACKAGE_PATTERN = r'[a-zA-Z0-9_\-]+'


class GStalkerServer(Application):

    def __init__(self, ioloop=None, config_path=None):
        urls = [
            (r'/', MainHandler),
            (r'/packages/(?P<package_name>{})'.format(PACKAGE_PATTERN), PackageHandler),
            (r'/chores/update_js_versions', RecalculateFromExactHandler)
        ]
        self.log = logger
        if config_path is None:
            self.config_path = './config/config.json'
        else:
            self.config_path = config_path
        self.config = load_config(self.config_path)

        self.db = scoped_session(sessionmaker(bind=engine(self.config['db'])))
        super(GStalkerServer, self).__init__(urls, debug=True, autoreload=False)


def main():
    app = GStalkerServer()

    try:
        http_server = HTTPServer(app)
        http_server.listen(8888, address='127.0.0.1')
        IOLoop.current().start()
    except (SystemExit, KeyboardInterrupt):
        pass

    http_server.stop()

    IOLoop.current().stop()
    sys.exit(0)


if __name__ == '__main__':
    main()
