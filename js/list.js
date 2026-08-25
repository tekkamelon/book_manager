// 検索ワードで一覧テーブルの行を絞り込む(grep -F -i相当)
function filterResult(word) {

	var rows = document.querySelectorAll('#result table tr');
	var keyword = word.toLowerCase();

	rows.forEach(function (row, index) {

		// 先頭行はヘッダーなので常に表示する
		if (index === 0) {
			row.removeAttribute('hidden');
			return;

		}

		// 固定文字列,大文字小文字を区別せず一致判定する
		if (row.textContent.toLowerCase().indexOf(keyword) !== -1) {
			row.removeAttribute('hidden');

		} else {
			row.setAttribute('hidden', '');

		}

	});

}

document.addEventListener('DOMContentLoaded', function () {

	// 一覧データを読み込んで表示する
	fetch('../cgi-bin/list.cgi')
		.then(function (response) {
			if (!response.ok) {
				throw new Error('HTTP status ' + response.status);
			}
			return response.text();
		})
		.then(function (html) {
			document.getElementById('result').innerHTML = html;
		})
		.catch(function (error) {
			document.getElementById('result').innerHTML =
				'<p class="result">読み込みに失敗しました: ' + error.message + '</p>';
		});

	// 検索フォームの送信でフィルタを実行する
	document.getElementById('search-form').addEventListener('submit', function (event) {
		event.preventDefault();
		filterResult(document.getElementById('q').value);
	});

});
