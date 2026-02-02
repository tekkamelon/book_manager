#!/bin/sh

# shellcheck disable=SC1090

set -eu

# 環境変数の設定
export LC_ALL=C
export LANG=C
export POSIXLY_CORRECT=1

# 変数を初期化
csv_file=""
search_str=""
search_result=""

# 設定ファイルのパス
config_file="../book_manager.conf"

# 設定ファイルから変数を読み込み
. ${config_file}

# 独自コマンドにパスを通す
export PATH="../bin:${PATH}"

# POSTリクエストでコンテンツ長がある場合
if [ "${REQUEST_METHOD:-GET}" = "POST" ] && [ -n "${CONTENT_LENGTH:-}" ]; then

	# POSTを変数に代入
	cat_post=$(cat)

	# "foo=bar"の"foo","bar"をそれぞれ抽出
	post_key="${cat_post%\=*}"
	post_value="${cat_post#"${post_key}"\=}"

	# POSTをデコード
	search_str=$(printf '%s' "${post_value}" | urldecode)

fi


# 関数の設定
# POSTを処理する関数
post_proc(){

	set +eu

	# 検索ワードが空でない場合に真
	if [ -n "${search_str}" ]; then

		# 固定文字列,大文字小文字を区別せず検索
		search_result=$(grep -F -i  "${search_str}" "${csv_file}") 

		# 検索結果があれば真
		if [ -n "${search_result}" ]; then

			# メッセージを表示
			printf '%s\n' "<p><strong>検索ワード: ${search_str}</strong></p>"

			# 検索結果をHTMLテーブルで表示
			printf '%s\n' "${search_result}"| c2h -v header=no

		else

			printf '%s\n' "<p><strong>検索ワード: ${search_str}に合致する結果はありません</strong></p>"

		fi

	else

		printf '%s\n' '<p class="result">検索ワードを入力してください。</p>'

	fi

}
# 関数の設定ここまで


set -eu

# HTML
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
	<h1>蔵書検索結果</h1>
	<p><a href="../html/index.html">トップ</a> | <a href="../html/search.html">検索</a> | <a href="../html/add.html">追加</a> | <a href="../html/settings.html">設定</a> </p>

	$(post_proc)

	</body>
</html>
EOF
# HTMLここまで
