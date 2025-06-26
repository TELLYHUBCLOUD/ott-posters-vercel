import * as cheerio from 'cheerio';

export default async function handler(req, res) {
  const { url, selector } = req.query;
  
  try {
    // Use a proxy API to fetch JS-rendered HTML
    const proxyUrl = `https://api.scraperapi.com?api_key=${process.env.SCRAPER_API_KEY}&url=${encodeURIComponent(url)}`;
    const response = await fetch(proxyUrl);
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
