#!/usr/bin/env python2

# import os
# import sympy
from sage import all as sage_all
from load_keys import load_key


def encrypt_message(message, public_key):
    if isinstance(public_key, object):

    try:
        public_exponent, modulus = load_key(public_key)
    except:
        public_exponent, modulus = public_key
    cipher_text = " ".join([str(sage_all.power_mod(ord(char), public_exponent, modulus)) for char in message])
    return cipher_text
    print("Entcrypted message: \n\n", cipher_text)
