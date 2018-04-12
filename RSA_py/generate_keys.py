#!/usr/bin/env python2

import os
# import sympy
from sage import all as sage_all


def rsa_keys():
    prime1, prime2 = gen_prime(), gen_prime()  # or 65537
    modulus = prime1 * prime2
    phi = (prime1 - 1) * (prime2 - 1)
    public_exponent = sage_all.random_prime(phi)
    private_exponent = sage_all.xgcd(public_exponent, phi)[1]  # to decrypt
    public_key = public_exponent, modulus
    private_key = private_exponent, modulus
    save_key("public", public_key)
    save_key("private", private_key)
    return public_key, private_key


def save_key(type, key):
    file_name = os.path.abspath("{}/{}.key".format(os.getcwd(), type))
    with open(file_name, "w+") as pkey:
        for i in key:
            pkey.write("{}\n".format(i))


def gen_prime():
    return sage_all.random_prime(2**1023, 2**1024)


def main():
    os.system("clear||cls")
    try:
        rsa_keys()
    except KeyboardInterrupt:
        os.sys.exit()


if __name__ == '__main__':
    main()
