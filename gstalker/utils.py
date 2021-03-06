# -*- coding: utf-8 -*-
import json
import re
import semver


def load_config(tgt_file):
    """Load the github auth data."""
    with open(tgt_file, 'r') as infile:
        config = json.load(infile)
    return config


def parse_for_meta(url):
    """Get the repo and username from a SHA commit file URL."""
    pat = re.compile('https:\/\/github.com\/([_\.\-a-zA-Z0-9]+)\/([_\.\-A-Za-z0-9]+)\/.*')
    matches = pat.match(url)
    if len(matches.groups()) == 2:
        return {
            'user': matches.groups()[0],
            'repo': matches.groups()[1]
        }
    else:
        return None


def parse_js_dep(key, value):
    # first we clean the value
    clean_value = ''
    for i in value:
        if i in '1234567890.':
            clean_value = clean_value + i
    try:
        sv = semver.parse(clean_value)
    except ValueError:
        major = 0
        minor = 0
        patch = 0
    else:
        major = sv['major']
        minor = sv['minor']
        patch = sv['patch']
    return {
        'dep_name': key,
        'exact_version': value,
        'min_major_ver': major,
        'min_minor_ver': minor,
        'min_patch_ver': patch
    }


def is_root_package_json(url):
    pat = re.compile('https:\/\/github.com\/([a-zA-Z0-9]+)\/([_\.\-A-Za-z0-9]+)\/raw/([a-f0-9]{40})/package.json')
    matches = pat.match(url)
    if matches is None:
        return False
    return True
