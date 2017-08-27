# -*- coding: utf-8 -*-
"""Query the database for things."""

import logging
import sys

import coloredlogs
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application

from gstalker.handlers import (
    MainHandler,
    PackageHandler
)

logger = logging.getLogger('gstalker_server')
coloredlogs.install(format='%(asctime)s - %(levelname)s: %(message)s', level='DEBUG', logger=logger)
PACKAGE_PATTERN = r'[a-zA-Z0-9_\-]+'


class GStalkerServer(Application):

    def __init__(self, ioloop=None):
        urls = [
            (r'/', MainHandler),
            (r'/packages/(?P<package_name>{})'.format(PACKAGE_PATTERN), PackageHandler),
        ]
        self.log = logger

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
