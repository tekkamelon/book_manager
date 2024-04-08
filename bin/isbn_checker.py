#!/usr/bin/env python3

import sys

# パイプからの標準入力を読み込み,改行コードの削除
input = sys.stdin.readline()
input = input.replace('\n', '')

# "input"をタプル化
num_tuple = tuple(input)

# "num_tuple"をint型にキャスト,"num_tuple_int"に代入
num_tuple_int = [int(i) for i in num_tuple]

# 奇数桁の合計
odd_num = sum(num_tuple_int[0::2])

# 偶数桁の合計の3倍
even_num = sum(num_tuple_int[1::2] * 3)

# 奇数桁と偶数桁の3倍を合計
addition = odd_num + even_num

# "addition"を10で割った剰余が0なら真,そうでなければ偽
if addition % 10 == 0:

    # 真の場合は入力内容をそのままを出力
    print(input)

else:

    # 偽の場合はエラーメッセージを出力,エラー終了
    sys.exit("Error: ISBN is bad!")
