document.addEventListener('DOMContentLoaded', function () {
	document.getElementById('helpButton').addEventListener('click', function () {
		console.log('ボタンがクリックされました');
		loadCodeServerUrl(function (url) {
			console.log('URL読み込み完了:', url);
			if (url) {
				console.log('URLに遷移します:', url);
				window.open(url, '_blank');
			} else {
				alert('code-serverのURLが設定されておりません');
			}
		});
	});
});