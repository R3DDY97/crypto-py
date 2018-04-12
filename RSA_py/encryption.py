#!/usr/bin/env python2

import os
# import sympy
from sage import all as sage_all
from load_keys import load_key


def encrypt_message(message, public_key):
    key_params = load_key(public_key)
    try:
        public_exponent, modulus = key_params or public_key
    except TypeError:
        print("wrong args")
        os.sys.exit()
    cipher_text = " ".join([str(sage_all.powermod(ord(char), public_exponent, modulus)) for char in message])
    return cipher_text
    print("Entcrypted message: \n\n", cipher_text)
