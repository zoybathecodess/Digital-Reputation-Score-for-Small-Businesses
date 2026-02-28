const https = require('https');
https.get('https://unpkg.com/recharts/umd/Recharts.js', (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => console.log(data.substring(0, 500)));
});
