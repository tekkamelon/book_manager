const { test, expect } = require('@playwright/test');

test.describe('confirm.html', () => {
	test('URLパラメータを確認画面に表示する', async ({ page }) => {
		await page.goto('/html/confirm.html?url=https%3A%2F%2Fexample.com');

		await expect(page.locator('#urlDisplay')).toHaveText('https://example.com');
		await expect(page.locator('#confirmButton')).toBeEnabled();
	});

	test('URLが未指定かつ未設定なら移動ボタンを無効にする', async ({ page }) => {
		await page.route('**/cgi-bin/api/settings.cgi', async (route) => {
			await route.fulfill({ json: {} });
		});
		await page.goto('/html/confirm.html');

		await expect(page.locator('#urlDisplay')).toHaveText('URLが指定されていません');
		await expect(page.locator('#confirmButton')).toBeDisabled();
	});
});
