#!/bin/sh

set -eu

# 環境変数設定
export LC_ALL=C
export LANG=C
export POSIXLY_CORRECT=1

# 設定ファイルから読み込み
config_file="/workspace/book_manager/book_manager.conf"
if [ -f "$config_file" ]; then
    . "$config_file"
    csv_file="$csv_file"
    script_dir="$script_dir"
else
    # フォールバック: ハードコードされたデフォルト値
    csv_file="/workspace/book_manager/data/library/library.csv"
    script_dir="/workspace/book_manager"
fi

export PATH="${script_dir}/bin:${PATH}"

# CGI POSTデータからisbn抽出
isbn=""

if [ "${REQUEST_METHOD:-GET}" = "POST" ] && [ -n "${CONTENT_LENGTH:-}" ]; then

	# POSTを変数に代入
	cat_post=$(cat)

	# "foo=bar"の"foo","bar"をそれぞれ抽出
	post_key="${cat_post%\=*}"
	post_value="${cat_post#"${post_key}"\=}"

	isbn=$(printf '%s' "${post_value}")

fi


# 関数の設定
post_proc(){

	if [ -z "${isbn}" ]; then

		echo '<p class="result">ISBNを入力してください。</p>'

	elif ! echo "${isbn}" | isbn_checker >/dev/null 2>&1; then

		printf '<p class="result">無効なISBN: %s</p>\n' "$(printf '%s' "${isbn}" | sed 's/&/\&amp;/g;s/</\</g;s/>/\>/g')"

	else

		# bm_search実行 (フォールバック有効)
		data=$(echo "${isbn}" | bm_search -f 2>/dev/null || echo "")

		if [ -z "${data}" ]; then

			printf '<p class="result">書籍情報が見つかりませんでした: %s</p>\n' "$(printf '%s' "${isbn}" | sed 's/&/\&amp;/g;s/</\</g;s/>/\>/g')"

		else

			# library.csvに追記(最後の行のみ,CSV形式確認)
			last_line=$(echo "${data}" | tail -1)

			if echo "${last_line}" | grep -q '^[^,]*,[^,]*,'; then

				echo "${last_line}" >> "${csv_file}"
				printf '<p class="result">成功: %s を追加しました。</p>\n' "$(printf '%s' "${isbn}" | sed 's/&/\&amp;/g;s/</\</g;s/>/\>/g')"
			  
				# 追加データをテーブル表示
				echo "${last_line}" | c2h -v header=no

			else

				echo '<p class="result">無効なデータ形式です。</p>'

			fi

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
	<p><a href="../html/search.html">検索</a> | <a href="../html/add.html">追加</a> | <a href="../html/index.html">メニュー</a></p>
<!-- EOF -->
	$(post_proc)

<!-- cat << EOF -->
	</body>
</html>
EOF
# HTMLここまで

