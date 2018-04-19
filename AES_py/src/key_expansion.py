#!/usr/bin/env python3


# import sys
from BitVector import *

AES_modulus = BitVector(bitstring='100011011')   # polynomials modulo --  x8 + x4 + x3 + x + 1


def get_round_keys():
    key_bv = get_key_from_user()
    key_words = gen_key_schedule_128(key_bv)

    key_schedule = []
    print("\nEach 32-bit word of the key schedule is shown as a sequence of 4 one-byte integers:")

    for index, word in enumerate(key_words):
        bits = [0, 8, 16, 24]
        keywords_as_int = [word[b:b + 8].intValue() for b in bits]
        if index % 4 == 0:
            print("\n")
        print("word %d:  %s" % (word_index, str(keywords_as_int)))
        key_schedule.append(keywords_as_int)

    round_keys = [None] * 11
    for i in range(11):
        round_keys[i] = (key_words[i * 4] + key_words[i * 4 + 1] + key_words[i * 4 + 2] +
                         key_words[i * 4 + 3]).get_bitvector_in_hex()
    print("\n\nRound keys in hex (first key for input block):\n")
    for round_key in round_keys:
        print(round_key)


def gee(keyword, round_constant, lookup_table):
    """function required to generate keywords."""

    rotated_word = keyword.deep_copy()
    rotated_word << 8
    newword = BitVector(size=0)
    for i in range(4):
        newword += BitVector(intVal=lookup_table[rotated_word[8 * i:8 * i + 8].intValue()], size=8)
    newword[:8] ^= round_constant
    round_constant = round_constant.gf_multiply_modular(BitVector(intVal=0x02), AES_modulus, 8)
    return newword, round_constant


def gen_key_schedule_128(key_bv):
    lookup_table = gen_subbytes_table()
    #  We need 44 keywords in the key schedule for 128 bit AES.  Each keyword is 32-bits
    #  wide. The 128-bit AES uses the first four keywords to xor the input block with.
    #  Subsequently, each of the 10 rounds uses 4 keywords from the key schedule. We will
    #  store all 44 keywords in the following list:
    key_words = [None for i in range(44)]
    round_constant = BitVector(intVal=0x01, size=8)
    for i in range(4):
        key_words[i] = key_bv[i * 32: i * 32 + 32]
    for i in range(4, 44):
        if i % 4 == 0:
            kwd, round_constant = gee(key_words[i - 1], round_constant, lookup_table)
            key_words[i] = key_words[i - 4] ^ kwd
        else:
            key_words[i] = key_words[i - 4] ^ key_words[i - 1]
    return key_words


def gen_subbytes_table():
    lookup_table = []
    c = BitVector(bitstring='01100011')

    for i in range(256):
        a = ac = BitVector(intVal=i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        a ^= (ac >> 4) ^ (ac >> 5) ^ (ac >> 6) ^ (ac >> 7) ^ c
        lookup_table.append(int(a))

    return lookup_table


def get_key_from_user():
    key = input("\nEnter key (16 chars):~> ").strip()
    req_len = 16

    if len(key) < req_len:
        key += '0' * (req_len - len(key))
    else:
        key = key[:req_len]

    key_bv = BitVector(textstring=key)
    return key_bv
