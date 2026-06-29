document.addEventListener('DOMContentLoaded', function () {
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
});
