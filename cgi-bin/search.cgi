#!/bin/sh

# 環境変数設定
export LC_ALL=C
export LANG=C
export POSIXLY_CORRECT=1

set -eu

# テストのためハードコード
csv_file="/home/tekkamelon/Documents/github/book_manager/data/library/library.csv"
script_dir="/home/tekkamelon/Documents/github/book_manager"
export PATH="${script_dir}/bin:${PATH}"

printf 'Content-Type: text/html; charset=UTF-8\r\n\r\n'

# CGI POSTデータからq抽出 (dd+tr/cutでPOSIX準拠)
q=""
if [ "${REQUEST_METHOD:-GET}" = "POST" ] && [ -n "${CONTENT_LENGTH:-}" ]; then

	# POSTを変数に代入
	cat_post=$(cat)

	# "foo=bar"の"foo","bar"をそれぞれ抽出
	post_key="${cat_post%\=*}"
	post_value="${cat_post#"${post_key}"\=}"

	# POSTをデコード
	q=$(printf '%s' "${post_value}" | urldecode)

fi

cat << EOF
<!DOCTYPE html>
<html lang="ja">
<head>
	<meta charset="UTF-8">
	<title>検索結果 - Book Manager</title>
	<link rel="stylesheet" href="../css/style.css">
</head>
<body>
	<h1>書籍検索結果</h1>
	<p><a href="../html/search.html">検索</a> | <a href="../html/index.html">メニュー</a></p>
EOF

if [ -n "${q}" ]; then

	printf '<p><strong>検索ワード: %s</strong></p>\n' "$(printf '%s' "${q}" | sed 's/&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g')"

	# grep -F でCSV検索しテーブル出力 (全フィールド固定文字列検索)
	grep -F "${q}" "${csv_file}" | c2h -v header=no

else

	echo '<p class="result">検索ワードを入力してください。</p>'

fi

cat << EOF
	</body>
</html>
EOF

