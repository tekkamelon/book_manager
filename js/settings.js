// 設定APIからJSONデータを取得する共通関数
function fetchSettings() {
	return fetch('../cgi-bin/api/settings.cgi')
		.then(response => {
			if (!response.ok) {
				throw new Error('HTTP error! status: ' + response.status);
			}
			return response.json();
		});
}

// 設定ファイルからcsv_fileの値を読み込む共通関数
function loadCsvFilePath(elementId, successPrefix, errorMessage) {
	fetchSettings()
		.then(data => {
			if (data.csv_file) {
				document.getElementById(elementId).textContent = successPrefix + data.csv_file;
			} else {
				document.getElementById(elementId).textContent = successPrefix + 'なし';
			}
		})
		.catch(error => {
			console.error(errorMessage, error);
			document.getElementById(elementId).textContent = successPrefix + '読み込み失敗';
		});
}

// 設定ファイルからcode-serverの値を読み込む関数
function loadCodeServerUrl(callback) {
	fetchSettings()
		.then(data => {
			const url = data.code_server || null;
			callback(url);
		})
		.catch(error => {
			console.error('code-serverの読み込みに失敗しました:', error);
			callback(null);
		});
}

// 設定ファイルからcsv_fileの値を読み込んでinput要素に設定する関数
function loadCsvFilePathToInput(inputId, labelId) {
	fetchSettings()
		.then(data => {
			if (data.csv_file) {
				document.getElementById(inputId).value = data.csv_file;
				document.getElementById(labelId).textContent = '現在の設定: ' + data.csv_file;
			} else {
				document.getElementById(labelId).textContent = '現在の設定: なし';
			}
		})
		.catch(error => {
			console.error('設定の読み込みに失敗しました:', error);
			document.getElementById(labelId).textContent = '現在の設定: 読み込み失敗';
		});
}

// 設定ファイルからcode-serverの値を読み込んでinput要素に設定する関数
function loadCodeServerUrlToInput(inputId, labelId) {
	fetchSettings()
		.then(data => {
			if (data.code_server) {
				document.getElementById(inputId).value = data.code_server;
				document.getElementById(labelId).textContent = '現在の設定: ' + data.code_server;
			} else {
				document.getElementById(labelId).textContent = '現在の設定: なし';
			}
		})
		.catch(error => {
			console.error('code-serverの読み込みに失敗しました:', error);
			document.getElementById(labelId).textContent = '現在の設定: 読み込み失敗';
		});
}
