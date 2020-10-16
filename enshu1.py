# "pip install python-Levenshtein" を実行する必要あり

import pandas as pd
import numpy as np
import Levenshtein as LV
import copy
import random

# 0-15(4bit)の数字に対応
class ED(object):
    def __init__(self):
        self.e_table, self.d_table = self._make_table()

    def encode(self, dec_num):
        code = self.e_table[str(dec_num)]
        return code
    
    def decode(self, code):
        FLAG = False
        cand = "?"
        for key in self.d_table:
            if LV.hamming(code,key) <= 1:
                if FLAG:
                    cand = "?"
                else:
                    cand = self.d_table[key]
                    FLAG = True
        return cand

    def denso(self, code, error_num=1, rand=False):
        max_len = len(code)

        SWAP_FLAG = True
        if rand:
            if random.randint(0, 1) == 0:
                SWAP_FLAG = False

        if SWAP_FLAG:
            swap_idx = random.randint(0, max_len)
            code = list(code)
            print("bf_denso: {}".format(code))

            if code[swap_idx] == "0":
                code[swap_idx] = "1"
            else:
                code[swap_idx] = "0"
            print("af_denso: {}".format(code))
            code = "".join(code)
        return code

    def _make_table(self, total=16):
        org_bin_list = []
        for num in range(total):
            bin = self._num_to_code(str(num), parity=True)
            org_bin_list.append(bin)

        df = pd.DataFrame(np.zeros((total, total)), dtype=object)
        for i in range(df.shape[0]):
            df[i][0] = org_bin_list[i]
        for j in range(df.shape[1]):
            df[0][j] = org_bin_list[j]

        # == 確認用 == #
        for i in range(1, df.shape[0]):
            for j in range(1, df.shape[1]):
                df[i][j] = LV.hamming(df[i][0], df[0][j])
        # print(df[0])
        # print(((df == 2)).sum())
        # ============ #

        e_table, d_table = {}, {}
        for i in range(len(df[0])):
            e_table[str(i)] = str(df[0][i])
            d_table[str(df[0][i])] = str(i)
        return e_table, d_table

    def _humming_code(self, bin_num):
        dig_list = [int(bin_num[i]) for i in range(len(bin_num))]

        parity_bits = []
        for (dr_idx, dig_rmv) in enumerate(dig_list):
            # parity_bitを最小に
            if (dr_idx + 1) == len(dig_list):
                break

            x = 0
            for (d_idx, dig) in enumerate(dig_list):
                if d_idx != dr_idx:
                    x += dig
            x = x % 2
            parity_bits.append(str(x))
        code = "".join(parity_bits)
        return code

    def _num_to_code(self, num, parity=False):
        bin_num = bin(int(num))
        bin_num = str(bin_num[2:]).zfill(4)

        if parity:
            hum_code = self._humming_code(bin_num)
            bin_num = bin_num + hum_code

        return bin_num


def main():
    test_num = 3

    ed = ED()
    enc_code = ed.encode(test_num)
    des_code = ed.denso(enc_code, error_num=1)
    dec_num = ed.decode(des_code)

    print("\n{} -> enc -> {} => denso => {} -> dec -> {}".format(test_num, enc_code, des_code, dec_num))
    print("\n=========\n")
    print("table: \n", ed.e_table)

main()