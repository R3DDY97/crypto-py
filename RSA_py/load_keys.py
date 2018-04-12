#!/usr/bin/env python2

import os


def load_key(key_file):
    try:
        file_path = os.path.abspath(key_file)
        if os.path.isfile(file_path):
            with open(file_path, "r+") as pkey:
                key_params = pkey.read()
            return key_params
    except TypeError:
        pass
    return None
