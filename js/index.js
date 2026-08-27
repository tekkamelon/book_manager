document.addEventListener('DOMContentLoaded', function () {
	const helpButton = document.getElementById('helpButton');
	const editorStatus = document.getElementById('editorStatus');

	helpButton.addEventListener('click', function () {
		loadCodeServerUrl(function (url) {
			if (url) {
				location.href = 'confirm.html?url=' + encodeURIComponent(url);
				return;
			}

			editorStatus.hidden = false;
			editorStatus.replaceChildren(
			'code-serverのURLが設定されていません。',
			Object.assign(document.createElement('a'), {
				href: 'settings.html',
				textContent: '設定画面で登録してください。',
			})
			);
		});
	});
});
