# -*- coding: utf-8 -*-


from tornado.web import RequestHandler


class RecalculateFromExactHandler(RequestHandler):
    """
        We recalculate the mins and maxes from the exact_version string in the database.
        Acts on every row in the database.
    """
    def get(self):
        self.write('Hello, world')
