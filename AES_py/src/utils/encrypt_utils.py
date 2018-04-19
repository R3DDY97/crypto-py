#!/usr/bin/env python3

# import os
# import math

# from sbox import (Sbox, InvSbox)

from sbox import Sbox


def str2bytes(text):
    btext = [ord(char) for char in text]
    return btext


def bytes2str(btext):
    text = [chr(bt) for bt in btext]
    return text


# learnt from http://cs.ucsb.edu/~koc/cs178/projects/JT/aes.c
def xtime(a):
    return (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)


def add_round_key(s, k):
    for i in range(4):
        for j in range(4):
            s[i][j] ^= k[i][j]


def round_encrypt(state_matrix, key_matrix):
    sub_bytes(state_matrix)
    shift_rows(state_matrix)
    mix_columns(state_matrix)
    add_round_key(state_matrix, key_matrix)


def sub_bytes(s):
    for i in range(4):
        for j in range(4):
            s[i][j] = Sbox[s[i][j]]


def shift_rows(s):
    s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]


def mix_single_column(a):
    # please see Sec 4.1.2 in The Design of Rijndael
    t = a[0] ^ a[1] ^ a[2] ^ a[3]
    u = a[0]
    a[0] ^= t ^ xtime(a[0] ^ a[1])
    a[1] ^= t ^ xtime(a[1] ^ a[2])
    a[2] ^= t ^ xtime(a[2] ^ a[3])
    a[3] ^= t ^ xtime(a[3] ^ u)


def mix_columns(s):
    for i in range(4):
        mix_single_column(s[i])
