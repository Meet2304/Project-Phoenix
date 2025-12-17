import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('https://project-phoenixx.vercel.app/');
  await page.getByRole('button', { name: 'Learn How' }).click();
  await page.getByRole('button', { name: 'Home' }).click();
  const page1Promise = page.waitForEvent('popup');
  await page.getByRole('button', { name: 'View on GitHub' }).click();
  const page1 = await page1Promise;
});