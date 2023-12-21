#!/bin/sh -eu

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

else

	# 偽の場合は終了
	exit 0

fi

surplus=$(

	echo "${isbn}" |

	# 1文字ずつフィールドに分割,isbnの左から奇数桁+偶数桁*3の剰余を求める
	awk -v FS='' '{

		print ($1 + $2 *3 + $3 + $4 * 3 + $5 + $6 * 3 + $7 + $8 * 3 + $9 + $10 * 3 + $11 + $12 * 3 + $13) % 10

	}'

)

# "surplus"が0であれば真,それ以外で偽
if [ "${surplus}" = 0 ] ; then

	# 真の場合はisbnを出力
	echo "${isbn}"

else

	# 偽の場合はメッセージを標準エラー出力に表示
	echo "ISBN is bad!" 1>&2

fi

