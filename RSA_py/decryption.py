#!/usr/bin/env python2

# import os
from sage import all as sage_all
from load_keys import load_key


def decrypt_message(cipher_text, private_key):
    try:
        private_exponent, modulus = load_key(private_key)
    except:
        private_exponent, modulus = private_key
    block_num = [(int(block)) for block in cipher_text.split()]
    decrypted_num = ""
    for block in block_num:
        message = sage_all.power_mod(block, private_exponent, modulus)
        decrypted_num += " " + str(message)
    message = "".join([chr(int(num)) for num in decrypted_num.split()])
    return message
    print("Decrypted message: \n\n", message)
