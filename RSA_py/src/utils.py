# from math import fmod


def int2hex(int):
    return hex(int)


def hex2int(hex_num):
    return int(hex_num, 16)


def str2hex(char):
    return hex(ord(char))


def hex2str(hex_str):
    return chr(int(hex_str), 16)


def fast_expo(base, expo, modulus):
    bin_expo = format(expo, "b")
    result = base
    for i in bin_expo:
        if int(i):
            result *= base
            result %= modulus
        result *= (base * base)
    return result


def fast_expo(base, expo):
    bin_expo = format(expo, "b")
    for i in bin_expo[1:]:
        if int(i):
            base *= base
        else:
            base *= base ** 2
    return base
