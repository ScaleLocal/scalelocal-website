// api/submit-guide.js — ScaleLocal content-offer lead capture
// Low-friction capture: a blog/AI-search reader requests the free Local SEO Checklist.
// This function:
//   1. Rejects bot submissions (honeypot)
//   2. Upserts a GHL contact tagged for the newsletter / nurture track
//      (NOT the sales opportunity pipeline — these are top-of-funnel contacts)
//   3. Returns ok so the page can reveal the download link
// A GHL workflow keyed off the `guide-download` tag handles the delivery email +
// newsletter nurture (see FREE_CHANNELS_PLAYBOOK.md §3).
//
// ENV VARS (Vercel project: scalelocal-website):
//   GHL_API_KEY — GHL Main sub-account Private Integration Token (already set)

const GHL_LOCATION_ID = 'cbDr5Xe384SCZnhPMvuZ';
const GHL_BASE = 'https://services.leadconnectorhq.com';

function ghlHeaders(key) {
  return {
    'Authorization': 'Bearer ' + key,
    'Version': '2021-07-28',
    'Content-Type': 'application/json',
  };
}

function splitName(full) {
  const t = (full || '').trim().split(/\s+/);
  if (t.length <= 1) return { firstName: t[0] || '', lastName: '' };
  return { firstName: t[0], lastName: t.slice(1).join(' ') };
}

function validEmail(e) {
  return typeof e === 'string' && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e.trim());
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const b = req.body || {};

  // 1. Honeypot — real users never fill `company_website`. Silently accept + drop.
  if (b.company_website && String(b.company_website).trim() !== '') {
    console.log('Honeypot triggered — dropping guide request');
    return res.status(200).json({ ok: true });
  }

  // Required: email only. Name optional (keep friction low).
  const email = (b.email || '').trim();
  if (!validEmail(email)) {
    return res.status(400).json({ error: 'A valid email is required' });
  }
  const fullName = (b.full_name || '').trim();
  const { firstName, lastName } = splitName(fullName);

  // which guide was requested (for tagging / future multi-offer use)
  const guide = (b.guide || 'local-seo-checklist').trim();

  const GHL_API_KEY = process.env.GHL_API_KEY;
  if (!GHL_API_KEY) {
    console.error('GHL_API_KEY not configured');
    return res.status(200).json({ ok: true, warning: 'Captured pending config' });
  }

  try {
    // 2. Upsert contact — newsletter/nurture track, NOT the sales pipeline.
    const upsertRes = await fetch(GHL_BASE + '/contacts/upsert', {
      method: 'POST',
      headers: ghlHeaders(GHL_API_KEY),
      body: JSON.stringify({
        locationId: GHL_LOCATION_ID,
        firstName,
        lastName,
        name: fullName || email,
        email,
        source: 'Content Offer — ' + guide,
        tags: ['guide-download', 'newsletter', 'guide-' + guide],
      }),
    });
    const upsertData = await upsertRes.json();
    console.log('GHL guide upsert:', upsertRes.status, JSON.stringify(upsertData).slice(0, 160));
    return res.status(200).json({ ok: true });
  } catch (err) {
    // Never fail the user — the page should still reveal the download.
    console.error('submit-guide error:', err && err.message);
    return res.status(200).json({ ok: true, warning: 'Captured with exception' });
  }
}
