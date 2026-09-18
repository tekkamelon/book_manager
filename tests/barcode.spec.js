const { test, expect } = require('@playwright/test');

/**
 * ライブカメラを使わずにバーコード読取の成否を検証するためのモック
 */
function installMock(page, decodedText) {
	return page.evaluate((text) => {
		window.Html5Qrcode = class FakeHtml5Qrcode {
			constructor() {}
			start(cameraConfig, scanConfig, successCallback) {
				return Promise.resolve().then(() => {
					successCallback(text, { decodedText: text });
				});
			}
			stop() {
				return Promise.resolve();
			}
			scanFile() {
				return Promise.reject(new Error('not mocked'));
			}
		};
	}, decodedText);
}

test.describe('ISBNバーコード読取 (add.html)', () => {
	test.beforeEach(async ({ page }) => {
		await page.goto('/html/add.html');
	});

	test('normalizeIsbn はハイフン付きの 978 ISBN を正規化する', async ({ page }) => {
		const result = await page.evaluate(() =>
			window.normalizeIsbn('978-4-7575-0620-6')
		);
		expect(result).toBe('9784757506206');
	});

	test('normalizeIsbn は価格コードを棄却する', async ({ page }) => {
		const result = await page.evaluate(() =>
			window.normalizeIsbn('1921234567890')
		);
		expect(result).toBeNull();
	});

	test('normalizeIsbn は 12桁の数字を棄却する', async ({ page }) => {
		const result = await page.evaluate(() =>
			window.normalizeIsbn('978475750620')
		);
		expect(result).toBeNull();
	});

	test('normalizeIsbn は文字混在を棄却する', async ({ page }) => {
		const result = await page.evaluate(() =>
			window.normalizeIsbn('9784757A506206')
		);
		expect(result).toBeNull();
	});

	test('読取成功時に ISBN 欄に 13桁が入力される', async ({ page }) => {
		await installMock(page, '9784757506206');

		await page.click('#barcode-start');

		await expect(page.locator('#isbn')).toHaveValue('9784757506206');
		await expect(page.locator('#barcode-preview')).toBeHidden();
	});

	test('価格コードは無視され ISBN 欄は空のまま', async ({ page }) => {
		// 192 始まりの 13桁 EAN(価格コード)。チェックデジットも合わせている
		await installMock(page, '1921234567895');

		await page.click('#barcode-start');
		await expect(page.locator('#barcode-start')).toHaveText('読み取りをやめる');

		await expect(page.locator('#isbn')).toHaveValue('');
		// ライブスキャンは停止せずプレビューを維持する(hidden 属性がない)
		expect(await page.locator('#barcode-preview').getAttribute('hidden')).toBeNull();
	});
});

test.describe('ISBNバーコード読取 (list.html)', () => {
	test.beforeEach(async ({ page }) => {
		await page.goto('/html/list.html');
		await page.waitForSelector('#result table');
	});

	test('読取成功時に検索欄へ ISBN が入り一覧が絞り込まれる', async ({ page }) => {
		// 一覧内に存在しない ISBN を使うと表示行が 1件(ヘッダーのみ)になる
		await installMock(page, '9780000000002');

		await page.click('#barcode-search-start');

		await expect(page.locator('#q')).toHaveValue('9780000000002');
		await expect(page.locator('#result table tr:not([hidden])')).toHaveCount(1);
	});
});
