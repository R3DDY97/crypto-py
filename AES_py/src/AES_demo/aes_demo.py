#!/usr/bin/env python3


import copy
from aes_constants import *


class Rijndael(object):

    def __init__(self, key, block_size=16):
        self.block_size = block_size

        ROUNDS = 10
        BC = int(block_size / 4)
        # encryption round keys
        Ke = [[0] * BC for i in range(ROUNDS + 1)]
        # decryption round keys
        Kd = [[0] * BC for i in range(ROUNDS + 1)]
        ROUND_KEY_COUNT = (ROUNDS + 1) * BC
        KC = int(len(key) / 4)

        # copy user material bytes into temporary ints
        tk = []
        for i in range(0, KC):
            tk.append((ord(key[i * 4]) << 24) | (ord(key[i * 4 + 1]) << 16) |
                      (ord(key[i * 4 + 2]) << 8) | ord(key[i * 4 + 3]))

        # copy values into round key arrays
        t = 0
        j = 0
        while j < KC and t < ROUND_KEY_COUNT:
            Ke[int(t / BC)][t % BC] = tk[j]
            Kd[ROUNDS - (int(t / BC))][t % BC] = tk[j]
            j += 1
            t += 1
        tt = 0
        rconpointer = 0
        while t < ROUND_KEY_COUNT:
            # extrapolate using phi (the round key evolution function)
            tt = tk[KC - 1]
            tk[0] ^= (S[(tt >> 16) & 0xFF] & 0xFF) << 24 ^  \
                     (S[(tt >> 8) & 0xFF] & 0xFF) << 16 ^  \
                     (S[tt & 0xFF] & 0xFF) << 8 ^  \
                     (S[(tt >> 24) & 0xFF] & 0xFF) ^  \
                     (rcon[rconpointer] & 0xFF) << 24
            rconpointer += 1
            if KC != 8:
                for i in range(1, KC):
                    tk[i] ^= tk[i - 1]
            else:
                for i in range(1, int(KC / 2)):
                    tk[i] ^= tk[i - 1]
                tt = tk[int(KC / 2 - 1)]
                tk[int(KC / 2)] ^= (S[tt & 0xFF] & 0xFF) ^ \
                    (S[(tt >> 8) & 0xFF] & 0xFF) << 8 ^ \
                    (S[(tt >> 16) & 0xFF] & 0xFF) << 16 ^ \
                    (S[(tt >> 24) & 0xFF] & 0xFF) << 24
                for i in range(int(KC / 2) + 1, KC):
                    tk[i] ^= tk[i - 1]
            # copy values into round key arrays
            j = 0
            while j < KC and t < ROUND_KEY_COUNT:
                Ke[int(t / BC)][t % BC] = tk[j]
                Kd[ROUNDS - (int(t / BC))][t % BC] = tk[j]
                j += 1
                t += 1
        # inverse MixColumn where needed
        for r in range(1, ROUNDS):
            for j in range(BC):
                tt = Kd[r][j]
                Kd[r][j] = U1[(tt >> 24) & 0xFF] ^ \
                    U2[(tt >> 16) & 0xFF] ^ \
                    U3[(tt >> 8) & 0xFF] ^ \
                    U4[tt & 0xFF]
        self.Ke = Ke
        self.Kd = Kd

    def encrypt(self, plaintext):
        if len(plaintext) != self.block_size:
            raise ValueError('wrong block length, expected ' + str(self.block_size) + ' got ' + str(len(plaintext)))
        Ke = self.Ke

        BC = 4
        ROUNDS = 10
        SC = 0

        s1 = shifts[SC][1][0]
        s2 = shifts[SC][2][0]
        s3 = shifts[SC][3][0]
        a = [0] * BC
        # temporary work array
        t = []
        # plaintext to ints + key
        for i in range(BC):
            t.append((ord(plaintext[i * 4]) << 24 |
                      ord(plaintext[i * 4 + 1]) << 16 |
                      ord(plaintext[i * 4 + 2]) << 8 |
                      ord(plaintext[i * 4 + 3])) ^ Ke[0][i])
        # apply round transforms
        for r in range(1, ROUNDS):
            for i in range(BC):
                a[i] = (T1[(t[i] >> 24) & 0xFF] ^
                        T2[(t[(i + s1) % BC] >> 16) & 0xFF] ^
                        T3[(t[(i + s2) % BC] >> 8) & 0xFF] ^
                        T4[t[(i + s3) % BC] & 0xFF]) ^ Ke[r][i]
            t = copy.deepcopy(a)
        # last round is special
        result = []
        for i in range(BC):
            tt = Ke[ROUNDS][i]
            result.append((S[(t[i] >> 24) & 0xFF] ^ (tt >> 24)) & 0xFF)
            result.append((S[(t[(i + s1) % BC] >> 16) & 0xFF] ^ (tt >> 16)) & 0xFF)
            result.append((S[(t[(i + s2) % BC] >> 8) & 0xFF] ^ (tt >> 8)) & 0xFF)
            result.append((S[t[(i + s3) % BC] & 0xFF] ^ tt) & 0xFF)
        return ''.join(list(map(chr, result)))

    def decrypt(self, ciphertext):
        if len(ciphertext) != self.block_size:
            raise ValueError('wrong block length, expected ' + str(self.block_size) + ' got ' + str(len(ciphertext)))
        Kd = self.Kd

        BC = int(self.block_size / 4)
        ROUNDS = len(Kd) - 1
        if BC == 4:
            SC = 0
        elif BC == 6:
            SC = 1
        else:
            SC = 2
        s1 = shifts[SC][1][1]
        s2 = shifts[SC][2][1]
        s3 = shifts[SC][3][1]
        a = [0] * BC
        # temporary work array
        t = [0] * BC
        # ciphertext to ints + key
        for i in range(BC):
            t[i] = (ord(ciphertext[i * 4]) << 24 |
                    ord(ciphertext[i * 4 + 1]) << 16 |
                    ord(ciphertext[i * 4 + 2]) << 8 |
                    ord(ciphertext[i * 4 + 3])) ^ Kd[0][i]
        # apply round transforms
        for r in range(1, ROUNDS):
            for i in range(BC):
                a[i] = (T5[(t[i] >> 24) & 0xFF] ^
                        T6[(t[(i + s1) % BC] >> 16) & 0xFF] ^
                        T7[(t[(i + s2) % BC] >> 8) & 0xFF] ^
                        T8[t[(i + s3) % BC] & 0xFF]) ^ Kd[r][i]
            t = copy.deepcopy(a)
        # last round is special
        result = []
        for i in range(BC):
            tt = Kd[ROUNDS][i]
            result.append((Si[(t[i] >> 24) & 0xFF] ^ (tt >> 24)) & 0xFF)
            result.append((Si[(t[(i + s1) % BC] >> 16) & 0xFF] ^ (tt >> 16)) & 0xFF)
            result.append((Si[(t[(i + s2) % BC] >> 8) & 0xFF] ^ (tt >> 8)) & 0xFF)
            result.append((Si[t[(i + s3) % BC] & 0xFF] ^ tt) & 0xFF)
        return ''.join(list(map(chr, result)))


r = Rijndael("abcdef1234567890", block_size=16)
ciphertext = r.encrypt("abcdef1234567890")
plaintext = r.decrypt(ciphertext)
print(plaintext, ciphertext)
