export default async function handler(req, res) {
  // CORS — allow scalelocal.net
  res.setHeader('Access-Control-Allow-Origin', 'https://scalelocal.net');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') { return res.status(200).end(); }
  if (req.method !== 'POST') { return res.status(405).json({ error: 'Method not allowed' }); }

  const { first_name, last_name, email, phone, business_name, city, industry } = req.body;

  if (!email || !first_name) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  const GHL_API_KEY = process.env.GHL_API_KEY;
  const GHL_LOCATION_ID = 'cbDr5Xe384SCZnhPMvuZ';

  try {
    // Create/update contact via GHL Contacts API v2
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
        lastName: last_name,
        email: email,
        phone: phone,
        companyName: business_name,
        city: city,
        source: 'Website Snapshot Request',
        customFields: [
          { key: 'industry', field_value: industry || '' }
        ],
        tags: ['snapshot-lead']
      })
    });

    const ghlData = await ghlRes.json();

    if (!ghlRes.ok) {
      console.error('GHL error:', JSON.stringify(ghlData));
      // Still return success to client — don't block the upsell flow
      return res.status(200).json({ ok: true, warning: 'GHL error but continuing' });
    }

    return res.status(200).json({ ok: true, contactId: ghlData.contact?.id });

  } catch (err) {
    console.error('Submit error:', err);
    return res.status(200).json({ ok: true, warning: 'Exception but continuing' });
  }
}
