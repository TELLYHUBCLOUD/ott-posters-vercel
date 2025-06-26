import { useState } from 'react';

export default function Home() {
  const [url, setUrl] = useState('');
  const [selector, setSelector] = useState('');
  const [posters, setPosters] = useState([]);

  const scrape = async () => {
    const res = await fetch(`/api/scrapePosters?url=${encodeURIComponent(url)}&selector=${encodeURIComponent(selector)}`);
    const data = await res.json();
    setPosters(data.posters || []);
  };

  return (
    <div style={{ padding: '40px' }}>
      <h1>🎬 OTT Poster Scraper</h1>
      <input value={url} onChange={e => setUrl(e.target.value)} placeholder="URL" />
      <input value={selector} onChange={e => setSelector(e.target.value)} placeholder="Selector" />
      <button onClick={scrape}>Scrape</button>
      <div>{posters.map((p, i) => <img key={i} src={p} width="150" />)}</div>
    </div>
  );
}
