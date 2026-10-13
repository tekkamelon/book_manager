// ISBNバーコード読取の共通モジュール
// html5-qrcode を使い、iOS Safari 等のカメラ映像から EAN-13 を解析する

(function () {
	'use strict';

	// ハイフン・空白を除去する
	var HYPHEN_OR_SPACE = /[-\s]/g;
	var DIGITS_13 = /^\d{13}$/;
	var ISBN_PREFIX = /^97[89]/;

	/**
	 * 読取文字列を ISBN-13(EAN-13) として正規化する
	 *
	 * @param {string} raw
	 * @returns {string|null} 正規化済み ISBN, または不合格の場合 null
	 */
	function normalizeIsbn(raw) {
		if (typeof raw !== 'string') {
			return null;
		}

		var cleaned = raw.replace(HYPHEN_OR_SPACE, '');

		if (!DIGITS_13.test(cleaned)) {
			return null;
		}

		if (!ISBN_PREFIX.test(cleaned)) {
			return null;
		}

		if (!isValidEan13(cleaned)) {
			return null;
		}

		return cleaned;
	}

	/**
	 * EAN-13 のチェックデジットを検証する
	 *
	 * @param {string} digits
	 * @returns {boolean}
	 */
	function isValidEan13(digits) {
		var sum = 0;
		for (var i = 0; i < 12; i += 1) {
			var digit = parseInt(digits.charAt(i), 10);
			// 奇数桁(1-indexed)は重み 1、偶数桁は重み 3
			var weight = (i % 2 === 0) ? 1 : 3;
			sum += digit * weight;
		}
		var check = (10 - (sum % 10)) % 10;
		return check === parseInt(digits.charAt(12), 10);
	}

	/**
	 * カメラ / 画像ファイルによる ISBN バーコード読取を起動する
	 *
	 * @param {Object} options
	 * @param {HTMLElement} options.trigger - 起動 / 停止ボタン
	 * @param {HTMLElement} options.preview - プレビュー描画先コンテナ
	 * @param {function(string):void} options.onSuccess - 正規化済み ISBN を受け取る
	 * @param {function(string):void} [options.onError] - エラーメッセージを受け取る
	 */
	function mountBarcodeReader(options) {
		var trigger = options.trigger;
		var preview = options.preview;
		var onSuccess = options.onSuccess || function () {};
		var onError = options.onError || function () {};

		if (!trigger || !preview) {
			console.error('mountBarcodeReader: trigger と preview は必須です');
			return;
		}

		var reader = null;
		var running = false;
		var stopped = false;
		var messageEl = null;
		var controlsEl = null;
		var fallbackInput = null;

		/**
		 * 一意な preview 要素 ID を保証する
		 */
		function ensurePreviewId() {
			if (!preview.id) {
				preview.id = 'barcode-preview-' + Date.now();
			}
			return preview.id;
		}

		/**
		 * ユーザー向けメッセージを表示する
		 */
		function showMessage(text, isError) {
			if (!messageEl) {
				return;
			}
			messageEl.textContent = text;
			messageEl.hidden = false;
			messageEl.classList.toggle('barcode-reader__message--error', !!isError);
		}

		function clearMessage() {
			if (messageEl) {
				messageEl.textContent = '';
				messageEl.hidden = true;
				messageEl.classList.remove('barcode-reader__message--error');
			}
		}

		function setRunning(state) {
			running = state;
			trigger.textContent = running ? '読み取りをやめる' : 'カメラからバーコードを読む';
			if (controlsEl) {
				controlsEl.hidden = running;
			}
		}

		/**
		 * カメラストリームを停止する
		 */
		function stop() {
			if (!reader || !running) {
				setRunning(false);
				preview.hidden = true;
				return Promise.resolve();
			}

			return reader.stop()
				.then(function () {
					setRunning(false);
					preview.hidden = true;
					clearMessage();
				})
				.catch(function () {
					setRunning(false);
					preview.hidden = true;
					showMessage('カメラの停止に失敗しました', true);
				});
		}

		/**
		 * 読取成功時のコールバック
		 */
		function handleDecoded(decodedText) {
			var isbn = normalizeIsbn(decodedText);
			if (!isbn) {
				// 価格コードや EAN-13 以外は無視してプレビューを継続する
				return;
			}

			if (stopped) {
				return;
			}
			stopped = true;

			stop().then(function () {
				onSuccess(isbn);
			});
		}

		/**
		 * カメラを起動する
		 */
		function start() {
			if (running) {
				return stop();
			}

			if (typeof window.Html5Qrcode === 'undefined') {
				var libError = 'バーコード読取ライブラリが読み込まれていません';
				showMessage(libError, true);
				onError(libError);
				return;
			}

			stopped = false;
			var previewId = ensurePreviewId();

			var formats = [];
			if (window.Html5QrcodeSupportedFormats &&
				window.Html5QrcodeSupportedFormats.EAN_13 !== undefined) {
				formats = [window.Html5QrcodeSupportedFormats.EAN_13];
			}

			try {
				reader = new window.Html5Qrcode(previewId, {
					verbose: false,
					formatsToSupport: formats,
				});
			} catch (err) {
				var initError = 'バーコード読取の準備に失敗しました';
				showMessage(initError, true);
				onError(initError);
				return;
			}

			preview.hidden = false;
			showMessage('カメラを起動しています...');

			var cameraConfig = { facingMode: 'environment' };
			var scanConfig = {
				fps: 10,
				disableFlip: true,
				aspectRatio: 1.7777778,
				qrbox: function (viewfinderWidth, viewfinderHeight) {
					var width = Math.min(280, viewfinderWidth - 16);
					var height = Math.min(120, viewfinderHeight - 16);
					return { width: width, height: height };
				},
			};

			reader.start(
				cameraConfig,
				scanConfig,
				function (decodedText) {
					handleDecoded(decodedText);
				},
				function (errorMessage, error) {
					// 解析不能フレームは通常運転なので無視する
					if (error && error.type === 2) {
						return;
					}
					// その他の一時的エラーもユーザーには通知しない
					if (window.console && console.debug) {
						console.debug('barcode scan debug:', errorMessage);
					}
				}
			).then(function () {
				setRunning(true);
				showMessage('ISBNバーコード(978/979)をかざしてください');
			}).catch(function () {
				preview.hidden = true;
				var cameraError = 'カメラを利用できません。ISBNを手入力してください。';
				showMessage(cameraError, true);
				onError(cameraError);
			});
		}

		/**
		 * 撮影した画像ファイルから ISBN を読み取る
		 */
		function scanFile(file) {
			if (!file) {
				return;
			}

			if (typeof window.Html5Qrcode === 'undefined') {
				var libError = 'バーコード読取ライブラリが読み込まれていません';
				showMessage(libError, true);
				onError(libError);
				return;
			}

			var previewId = ensurePreviewId();
			if (!reader) {
				var formats = [];
				if (window.Html5QrcodeSupportedFormats &&
					window.Html5QrcodeSupportedFormats.EAN_13 !== undefined) {
					formats = [window.Html5QrcodeSupportedFormats.EAN_13];
				}
				try {
					reader = new window.Html5Qrcode(previewId, {
						verbose: false,
						formatsToSupport: formats,
					});
				} catch (err) {
					var initError = 'バーコード読取の準備に失敗しました';
					showMessage(initError, true);
					onError(initError);
					return;
				}
			}

			preview.hidden = false;
			showMessage('画像を解析しています...');

			reader.scanFile(file, true)
				.then(function (decodedText) {
					var isbn = normalizeIsbn(decodedText);
					if (isbn) {
						preview.hidden = true;
						clearMessage();
						onSuccess(isbn);
					} else {
						showMessage(
							'ISBNバーコードが認識できませんでした。価格コードではなく ISBN側をかざしてください。',
							true
						);
					}
				})
				.catch(function () {
					showMessage('画像からバーコードを読み取れませんでした', true);
					onError('画像からバーコードを読み取れませんでした');
				})
				.finally(function () {
					if (fallbackInput) {
						fallbackInput.value = '';
					}
				});
		}

		/**
		 * trigger ボタンのクリックで起動 / 停止を切り替える
		 */
		trigger.addEventListener('click', function () {
			if (running) {
				stop();
			} else {
				start();
			}
		});

		/**
		 * ページを離れるときはカメラを確実に止める
		 */
		document.addEventListener('visibilitychange', function () {
			if (running && document.hidden) {
				stop();
			}
		});
		window.addEventListener('pagehide', function () {
			if (running) {
				stop();
			}
		});

		/**
		 * ライブスキャンが使えない場合のフォールバック UI を生成する
		 */
		function buildControls() {
			controlsEl = document.createElement('div');
			controlsEl.className = 'barcode-reader__controls';

			var fallbackButton = document.createElement('button');
			fallbackButton.type = 'button';
			fallbackButton.className = 'button button--secondary';
			fallbackButton.textContent = '写真から読む';

			fallbackInput = document.createElement('input');
			fallbackInput.type = 'file';
			fallbackInput.accept = 'image/*';
			fallbackInput.capture = 'environment';
			fallbackInput.className = 'barcode-reader__fallback-input';

			fallbackButton.addEventListener('click', function () {
				fallbackInput.click();
			});
			fallbackInput.addEventListener('change', function () {
				scanFile(fallbackInput.files[0]);
			});

			controlsEl.appendChild(fallbackButton);
			controlsEl.appendChild(fallbackInput);

			messageEl = document.createElement('p');
			messageEl.className = 'barcode-reader__message';
			messageEl.hidden = true;

			// html5-qrcode がプレビュー内を上書きするため、
			// コントロールとメッセージは preview の弟要素として配置する
			var parent = preview.parentNode;
			if (parent) {
				parent.insertBefore(controlsEl, preview.nextSibling);
				parent.insertBefore(messageEl, controlsEl.nextSibling);
			}
		}

		buildControls();
	}

	// テスト・ページ双方から利用できるよう公開する
	window.normalizeIsbn = normalizeIsbn;
	window.mountBarcodeReader = mountBarcodeReader;
})();
