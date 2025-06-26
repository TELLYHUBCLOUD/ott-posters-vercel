import puppeteer from 'puppeteer';

export default async function handler(req, res) {
  const { url, selector } = req.query;

  // Validate query params
  if (!url || !selector) {
    return res.status(400).json({ error: 'Missing url or selector parameter.' });
  }

  try {
    // Launch Puppeteer with bundled Chromium
    const browser = await puppeteer.launch({
      headless: 'new',
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();
    await page.goto(url, { waitUntil: 'networkidle2' });
    await page.waitForSelector(selector);

    const posters = await page.$$eval(selector, imgs => imgs.map(img => img.src));

    await browser.close();

    return res.status(200).json({ posters });
  } catch (err) {
    console.error('[Scrape Error]', err);
    return res.status(500).json({ error: err.message });
  }
}
