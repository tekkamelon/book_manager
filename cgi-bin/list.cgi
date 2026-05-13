#!/bin/sh

# shellcheck disable=SC1090

set -eu

export LC_ALL=C
export LANG=C
export POSIXLY_CORRECT=1

script_dir=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
export PATH="${script_dir}/../bin:${PATH}"

config_file="${script_dir}/../book_manager.conf"
csv_file=""

. "${config_file}"

html_escape() {
	printf '%s' "${1}" \
		| sed -e 's/&/\&amp;/g' -e 's/</\&lt;/g' -e 's/>/\&gt;/g'
}

render_table_fallback() {
	first_line=1
	printf '%s\n' '<div class="scroll-table">'
	printf '%s\n' '<table>'
	while IFS= read -r line || [ -n "${line}" ]; do
		escaped_line=$(html_escape "${line}")
		printf '%s\n' '<tr>'
		if [ "${first_line}" -eq 1 ]; then
			printf '%s\n' "${escaped_line}" \
				| awk -F',' '{for(i=1;i<=NF;i++) printf "<th>%s</th>\n", $i}'
			first_line=0
		else
			printf '%s\n' "${escaped_line}" \
				| awk -F',' '{for(i=1;i<=NF;i++) printf "<td>%s</td>\n", $i}'
		fi
		printf '%s\n' '</tr>'
	done < "${csv_file}"
	printf '%s\n' '</table>'
	printf '%s\n' '</div>'
}

render_csv_table() {
	if ! [ -f "${csv_file}" ]; then
		printf '%s\n' '<p class="result">データファイルが見つかりません</p>'
		return
	fi

	line_count=$(wc -l < "${csv_file}")
	if [ "${line_count}" -le 1 ]; then
		printf '%s\n' '<p class="result">蔵書データがありません</p>'
		return
	fi

	if command -v c2h >/dev/null 2>&1; then
		printf '%s\n' '<div class="scroll-table">'
		cat "${csv_file}" | c2h -v header=yes
		printf '%s\n' '</div>'
		return
	fi

	render_table_fallback
}

echo "Content-Type: text/html; charset=UTF-8"
echo ""

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
