#!/usr/bin/env python3


import copy
from aes_constants import *
from get_info import (get_message, get_key)


class Aes_128(object):

    def __init__(self):
        # def __init__(self, key):
        self.key = get_key()
        key = self.key
        # encryption round keys
        Ke = [[0] * 4 for i in range(11)]
        # decryption round keys
        Kd = [[0] * 4 for i in range(11)]

        # copy user material bytes into temporary ints
        tk = []
        for i in range(0, 4):
            tk.append((ord(key[i * 4]) << 24) | (ord(key[i * 4 + 1]) << 16) |
                      (ord(key[i * 4 + 2]) << 8) | ord(key[i * 4 + 3]))

        # copy values into round key arrays
        t = j = tt = 0

        while j < 4 and t < 44:
            Ke[int(t / 4)][t % 4] = tk[j]
            Kd[10 - (int(t / 4))][t % 4] = tk[j]
            j += 1
            t += 1

        rconpointer = 0
        while t < 44:
            # extrapolate using phi (the round key evolution function)
            tt = tk[4 - 1]
            tk[0] ^= (S[(tt >> 16) & 0xFF] & 0xFF) << 24 ^  \
                     (S[(tt >> 8) & 0xFF] & 0xFF) << 16 ^  \
                     (S[tt & 0xFF] & 0xFF) << 8 ^  \
                     (S[(tt >> 24) & 0xFF] & 0xFF) ^  \
                     (rcon[rconpointer] & 0xFF) << 24
            rconpointer += 1

            for i in range(1, 4):
                tk[i] ^= tk[i - 1]

            # copy values into round key arrays
            j = 0
            while j < 4 and t < 44:
                Ke[int(t / 4)][t % 4] = tk[j]
                Kd[10 - (int(t / 4))][t % 4] = tk[j]
                j += 1
                t += 1
        # inverse MixColumn where needed
        for r in range(1, 10):
            for i in range(4):
                tt = Kd[r][i]
                Kd[r][i] = U1[(tt >> 24) & 0xFF] ^ U2[(tt >> 16) & 0xFF] ^ \
                    U3[(tt >> 8) & 0xFF] ^ U4[tt & 0xFF]
        self.Ke = Ke
        self.Kd = Kd

    def aes_encrypt(self, message):
        block_list = get_message(message)
        ciphertext = ""
        for block in block_list:
            ciphertext += self.encrypt(block)
        print(ciphertext)
        return ciphertext

    def encrypt(self, plaintext):
        if len(plaintext) != 16:
            raise ValueError('wrong block length, expected {} got {}'.format(16, str(len(plaintext))))
        Ke = self.Ke

        s1 = shifts[1][0]
        s2 = shifts[2][0]
        s3 = shifts[3][0]
        a, t = [[0] * 4] * 2
        # temporary work array
        t = [0] * 4
        # plaintext to ints + key
        for i in range(4):
            t[i] = (ord(plaintext[i * 4]) << 24 |
                    ord(plaintext[i * 4 + 1]) << 16 |
                    ord(plaintext[i * 4 + 2]) << 8 |
                    ord(plaintext[i * 4 + 3])) ^ Ke[0][i]
        # apply round transforms
        for r in range(1, 10):
            for i in range(4):
                a[i] = (T1[(t[i] >> 24) & 0xFF] ^
                        T2[(t[(i + s1) % 4] >> 16) & 0xFF] ^
                        T3[(t[(i + s2) % 4] >> 8) & 0xFF] ^
                        T4[t[(i + s3) % 4] & 0xFF]) ^ Ke[r][i]
            t = copy.deepcopy(a)
        # last round is special
        result = []
        for i in range(4):
            tt = Ke[10][i]
            result.append((S[(t[i] >> 24) & 0xFF] ^ (tt >> 24)) & 0xFF)
            result.append((S[(t[(i + s1) % 4] >> 16) & 0xFF] ^ (tt >> 16)) & 0xFF)
            result.append((S[(t[(i + s2) % 4] >> 8) & 0xFF] ^ (tt >> 8)) & 0xFF)
            result.append((S[t[(i + s3) % 4] & 0xFF] ^ tt) & 0xFF)
        return ''.join(list(map(chr, result)))

    def aes_decrypt(self, cipher):
        cipher_list = [cipher[16 * i:(i + 1) * 16] for i in range(len(cipher) // 16)]
        plaintext = ""
        for block in cipher_list:
            plaintext += self.decrypt(block)
        print(plaintext)
        return plaintext

    def decrypt(self, ciphertext):
        if len(ciphertext) != 16:
            raise ValueError('wrong block length, expected expected {} got {}'.format(16, str(len(plaintext))))
        Kd = self.Kd

        s1 = shifts[1][1]
        s2 = shifts[2][1]
        s3 = shifts[3][1]
        a = [0] * 4
        t = [0] * 4

        # ciphertext to ints + key
        for i in range(4):
            t[i] = (ord(ciphertext[i * 4]) << 24 |
                    ord(ciphertext[i * 4 + 1]) << 16 |
                    ord(ciphertext[i * 4 + 2]) << 8 |
                    ord(ciphertext[i * 4 + 3])) ^ Kd[0][i]

        # apply round transforms
        for r in range(1, 10):
            for i in range(4):
                a[i] = (T5[(t[i] >> 24) & 0xFF] ^
                        T6[(t[(i + s1) % 4] >> 16) & 0xFF] ^
                        T7[(t[(i + s2) % 4] >> 8) & 0xFF] ^
                        T8[t[(i + s3) % 4] & 0xFF]) ^ Kd[r][i]
            t = copy.deepcopy(a)
        # last round is special
        result = []
        for i in range(4):
            tt = Kd[10][i]
            result.append((Si[(t[i] >> 24) & 0xFF] ^ (tt >> 24)) & 0xFF)
            result.append((Si[(t[(i + s1) % 4] >> 16) & 0xFF] ^ (tt >> 16)) & 0xFF)
            result.append((Si[(t[(i + s2) % 4] >> 8) & 0xFF] ^ (tt >> 8)) & 0xFF)
            result.append((Si[t[(i + s3) % 4] & 0xFF] ^ tt) & 0xFF)
        return ''.join(list(map(chr, result)))
