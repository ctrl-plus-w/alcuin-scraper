import puppeteer from 'puppeteer';

import { savePdf } from './utils/fs.util';

import urls from './constants/urls';

(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();

  await page.setViewport({ width: 1080, height: 1024 });

  await page.goto(urls.DEFAULT);
  savePdf('results/pdfs', 'screenshot', page);

  await browser.close();
})();
