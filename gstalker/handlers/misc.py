# -*- config: utf-8 -*-

import json
import time

from tornado.web import RequestHandler

from gstalker.models import Dependency


class MainHandler(RequestHandler):
    def get(self):
        self.write('Hello, world')


class PackageHandler(RequestHandler):

    def get(self, package_query):
        query = self.application.db.query(Dependency).filter_by(dep_name=package_query)
        ret_vals = {
            'time': time.time(),
            'matches': [_.serialize() for _ in query]
        }
        self.finish(json.dumps(ret_vals))
