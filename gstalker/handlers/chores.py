# -*- coding: utf-8 -*-


from tornado.web import RequestHandler

from gstalker.models import Dependency
from gstalker.utils import parse_js_dep


class RecalculateFromExactHandler(RequestHandler):
    """
        We recalculate the mins and maxes from the exact_version string in the database.
        Acts on every row in the database.
    """

    def get(self):
        session = self.application.db
        dependencies = session.query(Dependency).filter(Dependency.lang == 'js')
        for item in dependencies:
            item = parse_js_dep(item.dep_name, item.exact_version)
            session.add(item)
            session.flush()
            session.commit()
        # TODO
        self.finish('blah')
