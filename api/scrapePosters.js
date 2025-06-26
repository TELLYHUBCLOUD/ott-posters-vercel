import * as cheerio from 'cheerio';

export default async function handler(req, res) {
  const { url, selector } = req.query;
  if (!url || !selector) return res.status(400).json({ error: 'Missing params' });

  try {
    const response = await fetch(url);
    const html = await response.text();
    const $ = cheerio.load(html);
    
    const posters = $(selector)
      .map((_, img) => $(img).attr('src'))
      .get();

    res.status(200).json({ posters });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
}
