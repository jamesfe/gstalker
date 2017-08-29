# -*- config: utf-8 -*-

import json
import time

from tornado.web import RequestHandler
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from gstalker.models import Dependency


class HelperHandler(RequestHandler):

    def do_json_finish(self, message):
        self.finish(json.dumps(message))

    def session_commit(self):
        """Store the commit in the database."""
        try:
            self.application.db.flush()
            self.application.db.commit()
        except IntegrityError as err:
            self.application.log.error(err)
            self.db.rollback()
        except SQLAlchemyError as err:
            self.application.log.error(err)
            self.db.rollback()


class MainHandler(RequestHandler):
    def get(self):
        self.write('Hello, world')


class PackageHandler(HelperHandler):

    def get(self, package_query):
        query = self.application.db.query(Dependency).filter_by(dep_name=package_query)
        ret_vals = {
            'time': time.time(),
            'matches': [_.serialize() for _ in query]
        }
        self.do_json_finish(ret_vals)
