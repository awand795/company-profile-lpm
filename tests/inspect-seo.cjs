const http = require('http');

http.get('http://localhost:5000/', (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    const head = data.split('</head>')[0];
    console.log('=== TITLES ===');
    const titles = head.match(/<title[^>]*>.*?<\/title>/gi) || [];
    titles.forEach(t => console.log(' ', t));

    console.log('\n=== META DESCRIPTIONS ===');
    const descs = head.match(/<meta\s+name=["']description["'][^>]*>/gi) || [];
    descs.forEach(d => console.log(' ', d));

    console.log('\n=== CANONICALS ===');
    const canons = head.match(/<link\s+rel=["']canonical["'][^>]*>/gi) || [];
    canons.forEach(c => console.log(' ', c));

    console.log('\n=== THEME COLOR ===');
    const tcs = head.match(/<meta\s+name=["']theme-color["'][^>]*>/gi) || [];
    tcs.forEach(t => console.log(' ', t));

    console.log('\n=== OG TAGS ===');
    const ogs = head.match(/<meta\s+property=["']og:[^"']+["'][^>]*>/gi) || [];
    ogs.forEach(o => console.log(' ', o));

    console.log('\n=== TWITTER TAGS ===');
    const tws = head.match(/<meta\s+name=["']twitter:[^"']+["'][^>]*>/gi) || [];
    tws.forEach(t => console.log(' ', t));

    console.log('\n=== JSON-LD ===');
    const ld = head.match(/<script\s+type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi) || [];
    console.log('Count:', ld.length);
    ld.forEach((s, i) => console.log(`LD ${i}:\n`, s));

    console.log('\n=== HEADINGS (H1-H6) in body ===');
    const body = data.split('</head>')[1] || '';
    const hRegex = /<(h[1-6])\b([^>]*)>([\s\S]*?)<\/\1>/gi;
    let match;
    const headings = [];
    while ((match = hRegex.exec(body)) !== null) {
      const tag = match[1].toLowerCase();
      const text = match[3].replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
      headings.push({ tag, text });
    }
    console.log('Total Headings:', headings.length);
    headings.forEach(h => console.log(`  <${h.tag}>: "${h.text}"`));
  });
});
