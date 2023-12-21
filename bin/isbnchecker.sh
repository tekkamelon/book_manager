#!/bin/sh

# ====== 環境変数の設定 ======
# 環境変数の設定
export LC_ALL=C
export LANG=C

# GNU coreutilsの挙動をPOSIXに準拠
export POSIXLY_CORRECT=1
# ====== 環境変数の設定ここまで ======


# 標準入力の有無を確認,あれば真,無ければ偽
if [ -p /dev/stdin ] ; then

	# 真の場合は標準入力を変数に代入,非対話的に処理
	isbn=$(cat - )

else

	:

fi

mkfifo fifo_isbn fifo_math

echo "${isbn}" | fold -w1 > fifo_isbn &

cat << EOS > fifo_math &
+
*3+
+
*3+
+
*3+
+
*3+
+
*3+
+
*3+

EOS

paste -d "" fifo_isbn fifo_math | tr -d "\n" | awk '{print $0}' | bc

rm fifo_isbn fifo_math
