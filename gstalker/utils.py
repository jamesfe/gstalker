# -*- coding: utf-8 -*-
import json
import re


def load_config(tgt_file):
    """Load the github auth data."""
    with open(tgt_file, 'r') as infile:
        config = json.load(infile)
    return config


def parse_for_meta(url):
    """Get the repo and username from a SHA commit file URL."""
    pat = re.compile('https:\/\/github.com\/([a-z0-9]+)\/([a-z0-9]+)\/.*')
    matches = pat.match(url)
    if len(matches.groups()) == 2:
        return {
            'user': matches.groups()[0],
            'repo': matches.groups()[1]
        }
    else:
        return None
