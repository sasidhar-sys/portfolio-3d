import scrape from 'website-scraper';

const options = {
  urls: ['https://alche.studio/'],
  directory: './alche-download',
  request: {
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
  }
};

try {
  console.log('Starting download...');
  const result = await scrape(options);
  console.log(`Successfully downloaded ${result.length} resource(s)!`);
} catch (error) {
  console.error('Error downloading:', error);
}