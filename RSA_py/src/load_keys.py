#!/usr/bin/env python2

import os
import json


def load_key(key_file):
    file = os.path.abspath(key_file)
    if os.path.isfile(file):
        with open(file, "r+") as pkey:
            key_params = pkey.read()
        return key_params.splitlines()
    return None, None


def json_key(key_file):
    file = os.path.abspath(key_file)
    if os.path.isfile(file):
        with open(file, "r") as pkey:
            key_params = json.load(pkey)
        return key_params
    return None
