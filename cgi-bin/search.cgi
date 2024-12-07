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

file () {

	# 動作テストのためハードコード
	c2h /home/tekkamelon/Documents/library/library.csv | grep -F -v "<html>"

}

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

