export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') { return res.status(200).end(); }
  if (req.method !== 'POST') { return res.status(405).json({ error: 'Method not allowed' }); }

  const { first_name, last_name, email, phone, business_name, city, industry, source } = req.body;
  if (!email || !first_name) { return res.status(400).json({ error: 'Missing required fields' }); }

  // Tag and source logic based on which page submitted
  const src = source || 'snapshot';
  let ghlSource, tags;
  if (src === 'audit') {
    ghlSource = 'Website Audit Request';
    tags = ['audit-lead'];
  } else if (src === 'grow') {
    ghlSource = 'Website Grow Request';
    tags = ['grow-lead'];
  } else if (src === 'free-website') {
    ghlSource = 'Website Free-Website Request';
    tags = ['free-website-lead'];
  } else {
    ghlSource = 'Website Snapshot Request';
    tags = ['snapshot-lead'];
  }

  const GHL_API_KEY = process.env.GHL_API_KEY;
  const GHL_LOCATION_ID = 'cbDr5Xe384SCZnhPMvuZ';
  try {
    const ghlRes = await fetch('https://services.leadconnectorhq.com/contacts/', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + GHL_API_KEY,
        'Version': '2021-07-28',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        locationId: GHL_LOCATION_ID,
        firstName: first_name,
        lastName: last_name || '',
        email: email,
        phone: phone || '',
        companyName: business_name || '',
        city: city || '',
        source: ghlSource,
        tags: tags
      })
    });
    const ghlData = await ghlRes.json();
    console.log('GHL contacts response:', ghlRes.status, JSON.stringify(ghlData).substring(0, 200));
    if (!ghlRes.ok) { console.error('GHL contacts error:', ghlRes.status, JSON.stringify(ghlData)); }
    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('Submit error:', err.message);
    return res.status(200).json({ ok: true, warning: 'Exception but continuing' });
  }
}