// @ts-check
const { test, expect } = require('@playwright/test');

test.describe('蔵書一覧の検索機能', () => {

	test.beforeEach(async ({ page }) => {
		await page.goto('/html/list.html');
		await page.waitForSelector('#result table');
	});

	test('一覧テーブルが全件表示される', async ({ page }) => {
		const rows = page.locator('#result table tr');
		const visibleRows = page.locator('#result table tr:not([hidden])');

		expect(await rows.count()).toBeGreaterThan(1);
		await expect(visibleRows).toHaveCount(await rows.count());
	});

	test('検索ワードで行が絞り込まれる', async ({ page }) => {

		// 先頭のデータ行の内容を検索ワードに使う(データセットに依存しない)
		const firstDataRow = page.locator('#result table tr').nth(1);
		const keyword = (await firstDataRow.textContent()).trim();
		expect(keyword.length).toBeGreaterThan(0);

		await page.fill('#q', keyword);
		await page.click('input[type="submit"]');

		// 検索対象の行は表示されたまま
		await expect(firstDataRow).toBeVisible();

		// 表示行はすべて検索ワードを含み,非表示行はすべて含まない(grep -F -i相当)
		// なおヘッダー行(先頭)は常に表示するため検証対象から除外する
		const check = await page.evaluate((word) => {
			const lower = word.toLowerCase();
			const rows = Array.from(document.querySelectorAll('#result table tr'));
			const dataRows = rows.slice(1);

			return {
				total: rows.length,
				visibleCount: rows.filter((row) => !row.hasAttribute('hidden')).length,
				badVisible: dataRows.filter((row) =>
					!row.hasAttribute('hidden') &&
					row.textContent.toLowerCase().indexOf(lower) === -1).length,
				badHidden: dataRows.filter((row) =>
					row.hasAttribute('hidden') &&
					row.textContent.toLowerCase().indexOf(lower) !== -1).length,
			};
		}, keyword);

		expect(check.total).toBeGreaterThan(1);
		// ヘッダー行 + 少なくとも1件のデータ行
		expect(check.visibleCount).toBeGreaterThanOrEqual(2);
		expect(check.visibleCount).toBeLessThanOrEqual(check.total);
		expect(check.badVisible).toBe(0);
		expect(check.badHidden).toBe(0);

		// ヘッダー行は常に表示される
		await expect(page.locator('#result table tr').first()).toBeVisible();
	});

	test('大文字小文字を区別せずに検索できる', async ({ page }) => {

		// データ行からASCIIの単語とその行番号を探す(データセットに依存しない)
		// ヘッダー行の"ISBN"等を誤って採用しないようデータ行のみ対象にする
		const found = await page.evaluate(() => {
			const rows = Array.from(document.querySelectorAll('#result table tr'));

			for (let i = 1; i < rows.length; i++) {
				const match = rows[i].textContent.match(/[A-Za-z]{4,}/);
				if (match) {
					return { word: match[0], rowIndex: i };
				}
			}

			return { word: '', rowIndex: -1 };
		});

		test.skip(!found.word, 'テストデータにASCII単語が含まれないためスキップ');

		// 小文字にして検索しても元の語(大文字混じり)に合致する
		await page.fill('#q', found.word.toLowerCase());
		await page.click('input[type="submit"]');

		const visibleRows = page.locator('#result table tr:not([hidden])');
		expect(await visibleRows.count()).toBeGreaterThanOrEqual(2);

		// 元の単語を含む行が非表示になっていない
		const targetRow = page.locator('#result table tr').nth(found.rowIndex);
		await expect(targetRow).toBeVisible();
	});

	test('合致する結果がない場合はヘッダーのみ表示される', async ({ page }) => {
		await page.fill('#q', 'この検索に合致するデータは存在しないxyz12345');
		await page.click('input[type="submit"]');

		await expect(page.locator('#result table tr:not([hidden])')).toHaveCount(1);
	});

	test('空の検索ワードで再検索すると全件表示に戻る', async ({ page }) => {
		const totalRows = await page.locator('#result table tr').count();

		await page.fill('#q', '新潮社');
		await page.click('input[type="submit"]');
		expect(await page.locator('#result table tr:not([hidden])').count())
			.toBeLessThanOrEqual(totalRows);

		await page.fill('#q', '');
		await page.click('input[type="submit"]');

		await expect(page.locator('#result table tr:not([hidden])')).toHaveCount(totalRows);
	});

});
