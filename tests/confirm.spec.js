const { test, expect } = require('@playwright/test');

test.describe('confirm.html tests', () => {
	// サーバー起動を待つための setup
	test.beforeAll(async ({ request }) => {
		// サーバーが起動しているか確認
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
			await new Promise(resolve => setTimeout(resolve, 500));
			attempts++;
		}
		throw new Error('Server is not running at http://localhost:8000');
	});

	test('index.html から confirm.html に遷移し URL が表示される', async ({ page }) => {
		await page.goto('/html/index.html');

		// helpButton をクリック
		await page.locator('#helpButton').click();

		// confirm.html に遷移したことを確認
		await expect(page).toHaveURL(/confirm\.html/);

		// URLが表示されるまで待つ（settings.cgi の応答を待つ）
		await page.waitForSelector('#urlDisplay', { timeout: 10_000 });

		const urlText = await page.locator('#urlDisplay').textContent();
		expect(urlText).not.toBe('読み込み中...');
		expect(urlText).not.toBe('URLが指定されていません');
		expect(urlText).toMatch(/^https?:\/\//);

		// confirmButton が有効であることを確認
		await expect(page.locator('#confirmButton')).toBeEnabled();
	});

	test('search.html から confirm.html に遷移し URL が表示される', async ({ page }) => {
		await page.goto('/html/search.html');

		// nav の「編集」リンクをクリック
		await page.getByRole('link', { name: '編集' }).click();

		// confirm.html に遷移したことを確認
		await expect(page).toHaveURL(/confirm\.html/);

		// URLが表示されるまで待つ（settings.cgi の応答を待つ）
		await page.waitForSelector('#urlDisplay', { timeout: 10_000 });

		const urlText = await page.locator('#urlDisplay').textContent();
		expect(urlText).not.toBe('読み込み中...');
		expect(urlText).not.toBe('URLが指定されていません');
		expect(urlText).toMatch(/^https?:\/\//);

		// confirmButton が有効であることを確認
		await expect(page.locator('#confirmButton')).toBeEnabled();
	});

	test('list.html から confirm.html に遷移し URL が表示される', async ({ page }) => {
		await page.goto('/html/list.html');

		// nav の「編集」リンクをクリック
		await page.getByRole('link', { name: '編集' }).first().click();

		// confirm.html に遷移したことを確認
		await expect(page).toHaveURL(/confirm\.html/);

		// URLが表示されるまで待つ
		await page.waitForSelector('#urlDisplay', { timeout: 10_000 });

		const urlText = await page.locator('#urlDisplay').textContent();
		expect(urlText).not.toBe('読み込み中...');
		expect(urlText).not.toBe('URLが指定されていません');
		expect(urlText).toMatch(/^https?:\/\//);
	});

	test('add.html から confirm.html に遷移し URL が表示される', async ({ page }) => {
		await page.goto('/html/add.html');

		// nav の「編集」リンクをクリック
		await page.getByRole('link', { name: '編集' }).first().click();

		// confirm.html に遷移したことを確認
		await expect(page).toHaveURL(/confirm\.html/);

		// URLが表示されるまで待つ
		await page.waitForSelector('#urlDisplay', { timeout: 10_000 });

		const urlText = await page.locator('#urlDisplay').textContent();
		expect(urlText).not.toBe('読み込み中...');
		expect(urlText).not.toBe('URLが指定されていません');
		expect(urlText).toMatch(/^https?:\/\//);
	});

	test('settings.html から confirm.html に遷移し URL が表示される', async ({ page }) => {
		await page.goto('/html/settings.html');

		// nav の「編集」リンクをクリック
		await page.getByRole('link', { name: '編集' }).first().click();

		// confirm.html に遷移したことを確認
		await expect(page).toHaveURL(/confirm\.html/);

		// URLが表示されるまで待つ
		await page.waitForSelector('#urlDisplay', { timeout: 10_000 });

		const urlText = await page.locator('#urlDisplay').textContent();
		expect(urlText).not.toBe('読み込み中...');
		expect(urlText).not.toBe('URLが指定されていません');
		expect(urlText).toMatch(/^https?:\/\//);
	});
});
