#!/bin/sh

set -eu

# ====== 変数の設定 ======
# 環境変数の設定
export LC_ALL=C
export LANG=C
export POSIXLY_CORRECT=1

# 設定ファイルから読み込み
CONFIG_FILE="/workspace/book_manager/book_manager.conf"
if [ -f "$CONFIG_FILE" ]; then
    . "$CONFIG_FILE"
    csv_file="$CSV_FILE"
    script_dir="$SCRIPT_DIR"
else
    # フォールバック: ハードコードされたデフォルト値
    csv_file="/workspace/book_manager/data/library/library.csv"
    script_dir="/workspace/book_manager"
fi

export PATH="${script_dir}/bin:${PATH}"

# CGI POSTデータからq抽出 (dd+tr/cutでPOSIX準拠)
q=""

# POSTリクエストでコンテンツ長がある場合
if [ "${REQUEST_METHOD:-GET}" = "POST" ] && [ -n "${CONTENT_LENGTH:-}" ]; then

	# POSTを変数に代入
	cat_post=$(cat)

	# "foo=bar"の"foo","bar"をそれぞれ抽出
	post_key="${cat_post%\=*}"
	post_value="${cat_post#"${post_key}"\=}"

	# POSTをデコード,
	q=$(printf '%s' "${post_value}" | urldecode)

fi
# ====== 変数の設定ここまで ======


# ===== 関数の設定 ======
# POSTを処理する関数
post_proc(){

	if [ -n "${q}" ]; then

		printf '<p><strong>検索ワード: %s</strong></p>\n' "$(printf '%s' "${q}" | sed 's/&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g')"

		# 固定文字列で検索
		grep -F "${q}" "${csv_file}" | c2h -v header=no

	else

		echo '<p class="result">検索ワードを入力してください。</p>'

	fi

}
# ===== 関数の設定ここまで ======


# ====== HTML ======
echo "Content-Type: text/html; charset=UTF-8"
echo ""

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

	$(post_proc)

	</body>
</html>
EOF
# ====== HTMLここまで ======
