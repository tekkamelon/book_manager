// 設定ファイルからcsv_fileの値を読み込む共通関数
function loadCsvFilePath(elementId, successPrefix, errorMessage) {
	// CGIスクリプトから設定データを取得
	fetch('../cgi-bin/settings.cgi')
		.then(response => response.text())
		.then(html => {
			// HTMLをパースして現在のcsv_file値を抽出
			const parser = new DOMParser();
			const doc = parser.parseFromString(html, 'text/html');
			const preElement = doc.querySelector('pre');

			if (preElement) {
				const text = preElement.textContent;
				// 正規表現でcsv_fileの値を抽出
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
			// エラーが発生した場合の処理
			console.error(errorMessage, error);
			document.getElementById(elementId).textContent = `${successPrefix}読み込み失敗`;
			return null;
		});
}

// 設定ファイルからcode-serverの値を読み込む関数
function loadCodeServerUrl(callback) {
	console.log('code-server URLを読み込み開始');
	fetch('../cgi-bin/settings.cgi')
		.then(response => {
			console.log('CGIレスポンス受信:', response.status);
			return response.text();
		})
		.then(html => {
			console.log('受信したHTML:', html.substring(0, 200));
			const parser = new DOMParser();
			const doc = parser.parseFromString(html, 'text/html');
			const preElement = doc.querySelector('pre');

			if (preElement) {
			const text = preElement.textContent;
			console.log('pre要素の内容:', text);
			const match = text.match(/code_server=([^\n]+)/);
			if (match) {
				let url = match[1].replace(/&quot;/g, '"');
				url = url.replace(/^"|"$/g, '');
				console.log('抽出したURL:', url);
				callback(url);
				return;
			}
			console.log('code-serverが見つかりませんでした');
		} else {
				console.log('pre要素が見つかりませんでした');
			}
			callback(null);
		})
		.catch(error => {
			console.error('code-serverの読み込みに失敗しました:', error);
			callback(null);
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
				// 正規表現でcsv_fileの値を抽出
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
			// エラーが発生した場合の処理
			console.error('設定の読み込みに失敗しました:', error);
			document.getElementById(labelId).textContent = '現在の設定: 読み込み失敗';
			return null;
		});
}

// 設定ファイルからcode-serverの値を読み込んでinput要素に設定する関数
function loadCodeServerUrlToInput(inputId, labelId) {
	fetch('../cgi-bin/settings.cgi')
		.then(response => response.text())
		.then(html => {
			const parser = new DOMParser();
			const doc = parser.parseFromString(html, 'text/html');
			const preElement = doc.querySelector('pre');

			if (preElement) {
			const text = preElement.textContent;
			const match = text.match(/code_server=([^\n]+)/);
			if (match) {
				let url = match[1].replace(/&quot;/g, '"');
				url = url.replace(/^"|"$/g, '');
				document.getElementById(inputId).value = url;
				document.getElementById(labelId).textContent = `現在の設定: ${url}`;
				return url;
			}
		}
			document.getElementById(labelId).textContent = '現在の設定: なし';
			return null;
		})
		.catch(error => {
			console.error('code-serverの読み込みに失敗しました:', error);
			document.getElementById(labelId).textContent = '現在の設定: 読み込み失敗';
			return null;
		});
}
