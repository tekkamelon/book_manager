// @ts-check
const { test, expect } = require('@playwright/test');

const pages = [
	{ path: '/html/list.html', label: '蔵書一覧' },
	{ path: '/html/add.html', label: '書籍追加・データ検索' },
	{ path: '/html/confirm.html', label: '編集' },
	{ path: '/html/settings.html', label: '設定' },
	{ path: '/html/google_search.html', label: '書籍追加・データ検索' },
];

test.describe('ナビゲーションのタブハイライト', () => {
	test.beforeAll(async ({ request }) => {
		let attempts = 0;
		while (attempts < 10) {
			try {
				const response = await request.get('/html/index.html');
				if (response.status() === 200) {
					return;
				}
			} catch (e) {
				// サーバー未起動
			}
			await new Promise((resolve) => setTimeout(resolve, 500));
			attempts += 1;
		}
		throw new Error('Server is not running at http://localhost:8000');
	});

	for (const { path, label } of pages) {
		test(`${path} では「${label}」タブが現在ページとしてハイライトされる`, async ({ page }) => {
			await page.goto(path);

			const current = page.locator('body > .container > nav a[aria-current="page"]');
			await expect(current).toHaveCount(1);
			await expect(current).toHaveText(label);
			await expect(current).toBeVisible();
		});
	}

	test('非選択タブをクリックすると対応ページへ遷移する', async ({ page }) => {
		await page.goto('/html/add.html');
		await page.getByRole('navigation').getByRole('link', { name: '蔵書一覧' }).click();
		await expect(page).toHaveURL(/list\.html/);
		await expect(page.locator('body > .container > nav a[aria-current="page"]')).toHaveText('蔵書一覧');
	});

	test('CGIの一覧画面でも蔵書一覧タブがハイライトされる', async ({ page }) => {
		await page.goto('/cgi-bin/list.cgi');
		await expect(page.locator('body > nav a[aria-current="page"]')).toHaveText('蔵書一覧');
	});
});
