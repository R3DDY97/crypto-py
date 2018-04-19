#!/usr/bin/env python2

from sage import all as sage_all
# from load_keys import load_key
from load_keys import json_key


def encrypt_message(message, public_key):
    if isinstance(public_key, str):
        public_key = json_key(public_key)
    if not public_key:
        return None
    public_exponent, modulus = public_key

    cipher_text = " ".join([str(sage_all.power_mod(ord(char), public_exponent, modulus)) for char in message])
    return cipher_text
    # print("Entcrypted message: \n\n", cipher_text)
