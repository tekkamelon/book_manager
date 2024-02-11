#!/usr/bin/env python3

import sys

# パイプからの標準入力を読み込み,改行コードの削除
input = sys.stdin.readline()
input = input.replace('\n', '')

# "input"をリスト化
num_list = list(input)

# "num_list"をint型にキャスト,"num_list_int"に代入
num_list_int = []

for data in num_list:

    num_list_int.append(int(data))

# リストの要素数を取得
list_length = len(num_list)

odd_num = (num_list_int[0::2])

even_num = (num_list_int[1::2])

print(odd_num)
print(even_num)
# tmp = 0

# # "i"を0から"num_list"の要素数まで2ずつ増やす
# for i in range(0, list_length, 2):

#     sum_tmp = tmp + (num_list_int[i])

#     sum_tmp2 = sum_tmp + (num_list_int[i] + 2)
#     print(sum_tmp2)
