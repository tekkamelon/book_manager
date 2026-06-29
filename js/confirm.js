document.addEventListener('DOMContentLoaded', function () {
	const params = new URLSearchParams(window.location.search);
	const paramUrl = params.get('url');

	function setupConfirmPage(url) {
		document.getElementById('urlDisplay').textContent = url;
		document.getElementById('confirmButton').addEventListener('click', function () {
			window.open(url, '_blank');
			location.href = 'index.html';
		});
	}

	if (paramUrl) {
		setupConfirmPage(paramUrl);
	} else {
		loadCodeServerUrl(function (url) {
			if (url) {
				setupConfirmPage(url);
			} else {
				document.getElementById('urlDisplay').textContent = 'URLが指定されていません';
				document.getElementById('confirmButton').disabled = true;
			}
		});
	}
});
