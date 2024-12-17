#!/bin/sh

# e 返り値が0以外で停止
# u 未定義の変数参照で停止
# x 実行されたコマンドの出力
# v 変数の表示
set -eu

# ====== 変数の設定 ======
# ロケールの設定
export LC_ALL=C
export LANG=C

# GNU coreutilsの挙動をPOSIXに準拠
export POSIXLY_CORRECT=1

# 独自コマンドへPATHを通す
export PATH="$PATH:../bin"

# クエリをデコードし"search_str"に代入
search_str=$(echo "${QUERY_STRING#*\=}" | urldecode)

# csvファイル
# 動作テストのためハードコード
csv_file=/home/tekkamelon/Documents/library/library.csv
# ====== 変数の設定ここまで ======


# ===== 関数の宣言 ======
file () {

	# "search_str"があれば真
	if [ -n "${search_str}" ] ; then

		# 固定文字列かつ大文字小文字の区別をせずに検索
		grep -F -i "${search_str}" < "${csv_file}" | c2h -v header=no 

	else

		# csvファイルをhtml化し出力
		c2h -v header=no "${csv_file}"

	fi

}
# ===== 関数の宣言ここまで ======


echo "Content-type: text/html"
echo ""

cat << EOS
<html>

    <head>

        <meta charset="UTF-8" />
		<meta name="viewport" content="width=device-width,initial-scale=0.8">
		<link rel="stylesheet" href="https://newcss.net/new.min.css">
		<title>Result - Book Manager -</title>

    </head>

	<body>
		$(file)
	</body>

</html>
EOS

