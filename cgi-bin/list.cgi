#!/bin/sh

# shellcheck disable=SC1090

set -eu

# ====== 変数の宣言 ======
export LC_ALL=C
export LANG=C
export POSIXLY_CORRECT=1

# スクリプトの配置ディレクトリを取得する
script_dir=$(CDPATH="" cd -- "$(dirname "$0")" && pwd)

# プロジェクト固有のツールを含むbinディレクトリをPATHに追加する
export PATH="${script_dir}/../bin:${PATH}"

# 設定ファイルのパスを定義する
config_file="${script_dir}/../book_manager.conf"

# CSVファイルのパスは設定ファイルから読み込まれる
csv_file=""
# ====== 変数の宣言ここまで ======


# 設定ファイルを読み込む
. "${config_file}"


# ====== 関数の宣言 ======
# 引数で受け取った文字列のHTML特殊文字をエスケープする
html_escape() {
	printf '%s' "${1}" \
		| sed -e 's/&/\&amp;/g' -e 's/</\&lt;/g' -e 's/>/\&gt;/g'
}

# c2hコマンドが利用できない場合のテーブル描画処理
# CSVを手動でHTMLテーブルに変換する
render_table_fallback() {

	# 最初の行はヘッダーとして処理するフラグ
	first_line=1

	printf '%s\n' '<div class="scroll-table">'
	printf '%s\n' '<table>'

	# CSVファイルを1行ずつ読み込む
	while IFS= read -r line || [ -n "${line}" ]; do

		escaped_line=$(html_escape "${line}")
		printf '%s\n' '<tr>'

		if [ "${first_line}" -eq 1 ]; then

			# ヘッダー行をth要素として描画する
			printf '%s\n' "${escaped_line}" |

			awk -F',' '{for(i=1;i<=NF;i++) printf "<th>%s</th>\n", $i}'
			first_line=0

		else

			# データ行をtd要素として描画する
			printf '%s\n' "${escaped_line}" |

			awk -F',' '{for(i=1;i<=NF;i++) printf "<td>%s</td>\n", $i}'

		fi

		printf '%s\n' '</tr>'

	# CSVファイルを標準入力として渡す
	done < "${csv_file}"

	printf '%s\n' '</table>'
	printf '%s\n' '</div>'

}
# ====== 関数の宣言ここまで ======


# CSVデータをHTMLテーブルとして描画する
# c2hコマンドが利用可能な場合はそちらを使用し、
# ない場合はフォールバック処理を実行する
render_csv_table() {

	# CSVファイルの存在を確認する
	if ! [ -f "${csv_file}" ]; then

		printf '%s\n' '<p class="result">データファイルが見つかりません</p>'
		return

	fi

	# CSVファイルの行数を取得する
	line_count=$(wc -l < "${csv_file}")

	# ヘッダーのみの場合はデータがないとみなす
	if [ "${line_count}" -le 1 ]; then

		printf '%s\n' '<p class="result">蔵書データがありません</p>'
		return

	fi

	# c2hコマンドが利用可能か確認する
	if command -v c2h >/dev/null 2>&1; then

		printf '%s\n' '<div class="scroll-table">'

		# c2hコマンドでCSVをHTMLテーブルに変換する
		cat "${csv_file}" | c2h -v header=yes
		printf '%s\n' '</div>'
		return

	fi

	# c2hがない場合はフォールバック処理を実行する
	render_table_fallback

}

# HTTPヘッダーを出力する
echo "Content-Type: text/html; charset=UTF-8"
echo ""

# HTMLドキュメントを出力する
cat << EOF
<!DOCTYPE html>
<html lang="ja">
<head>
	<meta charset="UTF-8">
	<title>蔵書一覧 - Book Manager</title>
	<link rel="stylesheet" href="../css/style.css">
</head>
<body>
	<h1>蔵書一覧</h1>

	<nav>
		<a href="../html/index.html">トップ</a>
		<a href="../html/search.html">蔵書検索</a>
		<a href="../html/list.html">蔵書一覧</a>
		<a href="../html/add.html">書籍追加・データ検索</a>
		<a href="../html/confirm.html">編集(code-server)</a>
		<a href="../html/settings.html">設定</a>
	</nav>

	$(render_csv_table)

</body>
</html>
EOF
