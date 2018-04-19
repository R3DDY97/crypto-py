#!/usr/bin/env python3

# import os
# import math

# from sbox import (Sbox, InvSbox)
from sbox import InvSbox


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


def round_decrypt(state_matrix, key_matrix):
    add_round_key(state_matrix, key_matrix)
    inv_mix_columns(state_matrix)
    inv_shift_rows(state_matrix)
    inv_sub_bytes(state_matrix)


def inv_sub_bytes(s):
    for i in range(4):
        for j in range(4):
            s[i][j] = InvSbox[s[i][j]]


def inv_shift_rows(s):
    s[0][1], s[1][1], s[2][1], s[3][1] = s[3][1], s[0][1], s[1][1], s[2][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[1][3], s[2][3], s[3][3], s[0][3]


def inv_mix_column(s):
    # see Sec 4.1.3 in The Design of Rijndael
    for i in range(4):
        u = xtime(xtime(s[i][0] ^ s[i][2]))
        v = xtime(xtime(s[i][1] ^ s[i][3]))
        s[i][0] ^= u
        s[i][1] ^= v
        s[i][2] ^= u
        s[i][3] ^= v


def inv_mix_columns(s):
    for i in range(4):
        inv_mix_columns(s[i])
