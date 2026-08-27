// @ts-check
const { test, expect } = require('@playwright/test');

test.describe('トップページ', () => {
	test('主な操作と管理操作を区別して表示する', async ({ page }) => {
		await page.goto('/html/index.html');

		await expect(page.getByRole('banner')).toBeVisible();
		await expect(page.getByRole('main')).toBeVisible();
		await expect(page.getByRole('navigation', { name: 'メイン' })).toBeVisible();
		await expect(page.getByRole('heading', { name: '主な操作' })).toBeVisible();
		await expect(page.getByRole('link', { name: '蔵書一覧を見る' })).toBeVisible();
		await expect(page.getByRole('link', { name: '書籍をISBNで追加する' })).toBeVisible();
		await expect(page.getByRole('heading', { name: '管理' })).toBeVisible();
		await expect(page.getByRole('link', { name: '設定を変更する' })).toBeVisible();
	});

	test('編集環境が未設定なら設定画面への案内を表示する', async ({ page }) => {
		await page.route('**/cgi-bin/api/settings.cgi', async (route) => {
			await route.fulfill({ json: {} });
		});
		await page.goto('/html/index.html');
		await page.getByRole('button', { name: '外部で開く' }).click();

		const status = page.getByRole('status');
		await expect(status).toContainText('code-serverのURLが設定されていません');
		await expect(status.getByRole('link', { name: '設定画面で登録してください。' })).toHaveAttribute(
			'href',
			'settings.html'
		);
	});
});
