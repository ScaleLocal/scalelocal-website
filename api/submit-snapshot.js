export default async function handler(req, res) {
  // CORS — allow scalelocal.net
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') { return res.status(200).end(); }
  if (req.method !== 'POST') { return res.status(405).json({ error: 'Method not allowed' }); }

  const { first_name, last_name, email, phone, business_name, city, industry } = req.body;

  if (!email || !first_name) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  const FORM_ID = 'tfnHv9TG6B8I6gf6Varo';
  const GHL_LOCATION_ID = 'cbDr5Xe384SCZnhPMvuZ';

  try {
    // Submit via GHL form survey endpoint (no auth required)
    const formPayload = {
      formId: FORM_ID,
      locationId: GHL_LOCATION_ID,
      name: first_name + ' ' + (last_name || ''),
      email: email,
      phone: phone || '',
      field_lkdTq3JXTWcuK9JtIkqK: business_name || '',
      city: city || '',
      industry_6g0rbqdq: industry || '',
      formData: {
        first_name: first_name,
        last_name: last_name || '',
        email: email,
        phone: phone || '',
        business_name: business_name || '',
        city: city || '',
        industry: industry || ''
      }
    };

    const ghlRes = await fetch('https://backend.leadconnectorhq.com/forms/form-survey-event', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Referer': 'https://scalelocal.net/snapshot'
      },
      body: JSON.stringify(formPayload)
    });

    const ghlText = await ghlRes.text();
    console.log('GHL form response:', ghlRes.status, ghlText);

    if (!ghlRes.ok) {
      console.error('GHL form error:', ghlRes.status, ghlText);
    }

    // Always return success to client — don't block the upsell redirect
    return res.status(200).json({ ok: true });

  } catch (err) {
    console.error('Submit error:', err.message);
    return res.status(200).json({ ok: true, warning: 'Exception but continuing' });
  }
}