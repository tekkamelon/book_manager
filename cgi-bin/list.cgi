#!/bin/sh

# shellcheck disable=SC1090

set -eu

# ====== 変数の宣言 ======
export LC_ALL=C
export LANG=C
export POSIXLY_CORRECT=1

# プロジェクト固有のツールを含むbinディレクトリをPATHに追加する
export PATH="$(dirname "$0")/../bin:${PATH}"

# 設定ファイルのパスを定義する
config_file="$(dirname "$0")/../book_manager.conf"

# CSVファイルのパスは設定ファイルから読み込まれる
csv_file=""
# ====== 変数の宣言ここまで ======


# 設定ファイルを読み込む
. "${config_file}"


# ====== 関数の宣言 ======
# CSVデータをHTMLテーブルとして描画する
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

}
# ====== 関数の宣言ここまで ======


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
		<a href="../html/confirm.html">編集</a>
		<a href="../html/settings.html">設定</a>
	</nav>

	$(render_csv_table)

</body>
</html>
EOF