# -*- coding: utf-8 -*-

import unittest
import json

from gstalker.main import GStalker


class TestGStalkerMain(unittest.TestCase):

    def test_get_events_returns_json_object(self):
        item = GStalker(config_path='./config/config.json', init_db=False)
        res = item.get_events()
        self.assertIsNotNone(res)
        json_res = res.json()
        self.assertIsInstance(json_res, list)
        self.assertIsInstance(json_res[0], dict)

    def test_make_request_checks_remaining_requests(self):
        item = GStalker(config_path='./config/config.json', init_db=False)
        item.remaining_requests = -1
        item.make_api_request(item.event_url, auth=item.auth)

    def test_validate_commit(self):
        with open('./tests/test_data/bad_commit_for_validation.json', 'r') as t:
            test_payload = json.load(t)

        item = GStalker(config_path='./config/config.json', init_db=False)
        item.validate_commit(test_payload)
