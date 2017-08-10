# -*- coding: utf-8 -*-

import unittest

from gstalker.main import GStalker


class TestGStalkerMain(unittest.TestCase):

    def test_get_commit_makes_a_requests_call(self):
        pass

    def test_get_events_returns_json_object(self):
        item = GStalker(config_path='./config/config.json')
        res = item.get_events()
        self.assertIsNotNone(res)
        json_res = res.json()
        self.assertIsInstance(json_res, list)
        self.assertIsInstance(json_res[0], dict)

    def test_make_request_checks_remaining_requests(self):
        item = GStalker(config_path='./config/config.json')
        item.remaining_requests = -1
        item.make_request(item.event_url, auth=item.auth)

    def test_make_request_does_not_depend_on_reset_time(self):
        pass

    def test_parse_event_page_returns_only_push_events(self):
        pass

    def test_validate_commit_finds_right_files(self):
        pass
