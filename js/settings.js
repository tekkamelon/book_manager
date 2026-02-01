// 設定ファイルからcsv_fileの値を読み込む共通関数
function loadCsvFilePath(elementId, successPrefix, errorMessage) {
	fetch('../cgi-bin/settings.cgi')
		.then(response => response.text())
		.then(html => {
			// HTMLから現在のcsv_file値を抽出
			const parser = new DOMParser();
			const doc = parser.parseFromString(html, 'text/html');
			const preElement = doc.querySelector('pre');

			if (preElement) {
				const text = preElement.textContent;
				const match = text.match(/csv_file=([^\n]+)/);
				if (match) {
					const currentPath = match[1].replace(/&quot;/g, '"');
					document.getElementById(elementId).textContent = `${successPrefix}${currentPath}`;
					return currentPath;
				}
			}
			document.getElementById(elementId).textContent = `${successPrefix}なし`;
			return null;
		})
		.catch(error => {
			console.error(errorMessage, error);
			document.getElementById(elementId).textContent = `${successPrefix}読み込み失敗`;
			return null;
		});
}

// 設定ファイルからcsv_fileの値を読み込んでinput要素に設定する関数
function loadCsvFilePathToInput(inputId, labelId) {
	fetch('../cgi-bin/settings.cgi')
		.then(response => response.text())
		.then(html => {
			// HTMLから現在のcsv_file値を抽出
			const parser = new DOMParser();
			const doc = parser.parseFromString(html, 'text/html');
			const preElement = doc.querySelector('pre');

			if (preElement) {
				const text = preElement.textContent;
				const match = text.match(/csv_file=([^\n]+)/);
				if (match) {
					const currentPath = match[1].replace(/&quot;/g, '"');
					document.getElementById(inputId).value = currentPath;
					document.getElementById(labelId).textContent = `現在の設定: ${currentPath}`;
					return currentPath;
				}
			}
			document.getElementById(labelId).textContent = '現在の設定: なし';
			return null;
		})
		.catch(error => {
			console.error('設定の読み込みに失敗しました:', error);
			document.getElementById(labelId).textContent = '現在の設定: 読み込み失敗';
			return null;
		});
}
