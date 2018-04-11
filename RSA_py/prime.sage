#!/usr/bin/env python2

from sage.all import *


def rsa_keys():
    p = random_prime(2**512)
    q = random_prime(2**512)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random_prime(phi)
    d = xgcd(e, phi)[1]
    public_key = e, n
    private_key = d, n
    return public_key, private_key


def encrypt(message):
    public_key, private_key = rsa_keys()
    public exponet, modulus = public_key
    cipher_text = power_mod(text, public_exponet, modulus)
    print("Entcrypted message: \n\n", cipher_text)


def decrypt(cipher_text):
    public_key, private_key = rsa_keys()
    private_exponent, modulus = private_key
    message = power_mod(cipher_text, private_exponent, modulus)
    print("Decrypted message: \n\n", message)
