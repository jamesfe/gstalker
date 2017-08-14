# -*- coding: utf-8 -*-

import unittest
import json

from gstalker.main import GStalker
from gstalker.models import RepositoryMoment


class TestStoreCommit(unittest.TestCase):

    def test_validate_commit_fails_on_non_list(self):
        item = GStalker(init_db=False)
        with self.assertRaises(AssertionError):
            item.validate_commit('blah')

    def test_validate_commit(self):
        item = GStalker(init_db=False)
        with open('./tests/test_data/commit_with_removed_tgt_file.json', 'r') as t:
            test_payload = json.load(t)
        res = item.validate_commit(test_payload)
        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0], dict)
        expected = {
            'repo_name': u'expressmongooserestapi',
            'sha': u'8f57f8bcd08e3e3ba53e43e971db98957097d95b',
            'user': u'xuqianjin',
            'repo_type': 'package.json',
            'check_state': 'FOUND',
            'target_file_url': u'https://github.com/xuqianjin/ExpressMongooseRestApi/raw/3b96ee2ec03212613bb3509a7d0f0cdad120bce6/package.json'
        }
        self.assertDictEqual(res[0], expected)
        self.assertEqual(len(res), 1)

    def test_insert_actually_works(self):
        item = GStalker(init_db=True)
        with open('./tests/test_data/package_json_added_with_dashes_in_repo_name.json', 'r') as t:
            test_payload = json.load(t)
        items = item.db.query(RepositoryMoment).count()
        commits = item.validate_commit(test_payload)
        for val in commits:
            item.store_commit(val)
        self.assertEqual(items + 1, item.db.query(RepositoryMoment).count())
