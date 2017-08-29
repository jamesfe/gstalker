# -*- coding: utf-8 -*-

import time

from gstalker.models import Dependency
from gstalker.utils import parse_js_dep
from gstalker.handlers import HelperHandler


class RecalculateFromExactHandler(HelperHandler):
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

        self.session_commit()

        ret_values = {
            'timestamp': time.time(),
            'result': 'success'
        }
        self.do_json_finish(ret_values)
