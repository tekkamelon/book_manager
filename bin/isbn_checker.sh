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

	# 真の場合は標準入力を変数に代入
	isbn=$(cat - )

	# 名前付きパイプを作成
	mkfifo isbn.fifo math.fifo

else

	# 偽の場合は終了
	exit 0

fi

set -eu
# "isbn"をタテにして名前付きパイプへリダイレクト
echo "${isbn}" | fold -w1 > isbn.fifo &

# isbnが正しいかをチェックする式を出力,名前付きパイプへリダイレクト
cat << EOS > math.fifo &
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

# isbnの左から奇数桁+偶数桁*3の剰余を求める
surplus=$(

	# 区切り文字を無しに指定,isbn.fifoとmath.fifoを結合
	paste -d "" isbn.fifo math.fifo |

	# 改行を削除,式を"()"でくくり行末に剰余を求める式を追加,bcで計算
	tr -d "\n" | xargs -I{} echo "({})%10" | bc

)

# "surplus"が0であれば真,それ以外で偽
if [ "${surplus}" = 0 ] ; then

	# 真の場合はisbnを出力
	echo "${isbn}"

else

	# 偽の場合はメッセージを標準エラー出力に表示
	echo "ISBN is bad!" 1>&2

fi

# 名前付きパイプを削除
rm isbn.fifo math.fifo

