# -*- coding: utf-8 -*-

import unittest

from gstalker.utils import parse_for_meta, is_root_package_json


class TestStoreCommit(unittest.TestCase):

    def test_parse_for_metadata_includes_dashes(self):
        url = 'https://github.com/therodan/typescript-web-starterkit/raw/a7565173719bff61c5910d6fcdbdf8de2ff90374/package.json'
        res = parse_for_meta(url)
        self.assertEqual(res['user'], 'therodan')
        self.assertEqual(res['repo'], 'typescript-web-starterkit')

    def test_parse_for_metadata(self):
        url = 'https://github.com/xuqianjin/ExpressMongooseRestApi/raw/3b96ee2ec03212613bb3509a7d0f0cdad120bce6/package.json'
        res = parse_for_meta(url)
        self.assertEqual(res['user'], 'xuqianjin')
        self.assertEqual(res['repo'], 'ExpressMongooseRestApi')

    def test_parse_for_metadata_includes_dots(self):
        url = 'https://github.com/selfsun/selffun.github.io/commits/c04b63c3d04814363d22d764c717edb41bb1a971'
        res = parse_for_meta(url)
        self.assertEqual(res['user'], 'selfsun')
        self.assertEqual(res['repo'], 'selffun.github.io')

    def test_parse_for_metadata_includes_underscores(self):
        url = 'https://github.com/cao5zy/design_microservice/commits/87effaafd92250582155574703a46eb2612687d8'
        res = parse_for_meta(url)
        self.assertEqual(res['user'], 'cao5zy')
        self.assertEqual(res['repo'], 'design_microservice')

    def test_is_root_packags(self):
        good = ['https://github.com/therodan/typescript-web-starterkit/raw/a7565173719bff61c5910d6fcdbdf8de2ff90374/package.json',
                'https://github.com/xuqianjin/ExpressMongooseRestApi/raw/3b96ee2ec03212613bb3509a7d0f0cdad120bce6/package.json']
        for item in good:
            self.assertTrue(is_root_package_json(item))

    def test_is_not_root_packags(self):
        good = ['https://github.com/therodan/typescript-web-starterkit/raw/a7565173719bff61c5910d6fcdbdf8de2ff90374/blah/blah/package.json',
                'https://github.com/xuqianjin/ExpressMongooseRestApi/raw/3b96ee2ec03212613bb3509a7d0f0cdad120bce6/node_modules/package.json']
        for item in good:
            self.assertFalse(is_root_package_json(item))
