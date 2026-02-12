#!/bin/sh

# shellcheck disable=SC1090

set -eu

# 環境変数設定
export LC_ALL=C
export LANG=C
export POSIXLY_CORRECT=1

# 変数を初期化
csv_file=""
isbn=""
add_to_csv="no"

# 設定ファイルのパス
config_file="../book_manager.conf"

# 設定ファイルから変数を読み込み
. ${config_file}

# 独自コマンドにパスを通す
export PATH="../bin:${PATH}"

if [ "${REQUEST_METHOD:-GET}" = "POST" ] && [ -n "${CONTENT_LENGTH:-}" ]; then

	# POSTデータを変数に代入
	cat_post=$(cat)

	# isbnを抽出
	isbn=$(printf '%s' "${cat_post}" | sed 's/.*isbn=\([^&]*\).*/\1/')

	# add_to_csvを抽出（デフォルトno）
	add_to_csv=$(printf '%s' "${cat_post}" | sed -n 's/.*add_to_csv=\([^&]*\).*/\1/p')

	if [ -z "${add_to_csv}" ]; then
		add_to_csv="no"
	fi

fi


# 関数の設定
post_proc(){

	# bm_search実行 (フォールバック有効)
	data=$(echo "${isbn}" | bm_search -f 2>/dev/null || echo "")

	if [ -z "${data}" ]; then

		printf '<p class="result">書籍情報が見つかりませんでした: %s</p>\n' "$(printf '%s' "${isbn}" | sed 's/&/\&amp;/g;s/</\</g;s/>/\>/g')"

	else

		last_line=$(echo "${data}" | tail -1)

		if echo "${last_line}" | grep -q '^[^,]*,[^,]*,'; then

			if [ "${add_to_csv}" = "yes" ]; then

				echo "${last_line}" >> "${csv_file}"
				printf '<p class="result">成功: %s を追加しました</p>\n' "$(printf '%s' "${isbn}" | sed 's/&/\&amp;/g;s/</\</g;s/>/\>/g')"
			else

				printf '<p class="result">成功: %s の情報を取得しました(CSV追加なし)</p>\n' "$(printf '%s' "${isbn}" | sed 's/&/\&amp;/g;s/</\</g;s/>/\>/g')"

			fi

			# 取得データをテーブル表示
			echo "${last_line}" | c2h -v header=no

			# 書影を取得・表示
			cover_url=$(echo "${isbn}" | bm_cover 2>/dev/null || echo "")
			if [ -n "${cover_url}" ]; then
				printf '<div class="cover-image"><img src="%s" alt="書影" style="max-width:200px;max-height:300px;margin-top:20px;"></div>\n' "${cover_url}"
			fi

		else

			echo '<p class="result">無効なデータ形式です</p>'

		fi

	fi

}
# 関数の設定ここまで=


# HTML
echo "Content-Type: text/html; charset=UTF-8"
echo ""

cat << EOF
<!DOCTYPE html>
<html lang="ja">
<head>
	<meta charset="UTF-8">
	<title>追加結果 - Book Manager</title>
	<link rel="stylesheet" href="../css/style.css">
</head>
<body>
	<h1>書籍追加結果</h1>
	<p><a href="../html/search.html">検索</a> | <a href="../html/add.html">追加</a> | <a href="../html/settings.html">設定</a> | <a href="../html/index.html">メニュー</a></p>
<!-- EOF -->
	$(post_proc)

<!-- cat << EOF -->
	</body>
</html>
EOF
# HTMLここまで

