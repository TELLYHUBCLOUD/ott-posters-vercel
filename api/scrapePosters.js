import puppeteer from 'puppeteer';

export default async function handler(req, res) {
  const { url, selector } = req.query;
  if (!url || !selector) return res.status(400).json({ error: 'Missing params' });

  try {
    const browser = await puppeteer.launch({
  headless: "new",
  executablePath: process.env.CHROME_BIN || '/usr/bin/google-chrome',
  args: ['--no-sandbox', '--disable-setuid-sandbox']
});

    const page = await browser.newPage();
    await page.goto(url, { waitUntil: 'networkidle2' });
    await page.waitForSelector(selector);
    const posters = await page.$$eval(selector, imgs => imgs.map(img => img.src));
    await browser.close();
    res.status(200).json({ posters });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
}
