# -*- coding: utf-8 -*-
import json


def load_config(tgt_file):
    """Load the github auth data."""
    with open(tgt_file, 'r') as infile:
        config = json.load(infile)
    return config
