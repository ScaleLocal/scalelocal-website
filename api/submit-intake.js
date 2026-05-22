// api/submit-intake.js — ScaleLocal Growth Plan Intake handler
// The custom /get-started/ form POSTs here. This function:
//   1. Rejects bot submissions (honeypot)
//   2. Upserts a GHL contact with all intake + UTM custom fields
//   3. Creates an Opportunity in the "Inbound Plan Requests" pipeline at "New Request"
//   4. Returns ok so the page can show its confirmation view
// GHL workflows "Inbound — Prospect SMS Ack" and "Inbound — Notify Matt" trigger off
// the form/opportunity and handle the prospect SMS + Matt notification.
//
// ENV VARS REQUIRED (Vercel project: scalelocal-website):
//   GHL_API_KEY            — GHL Main sub-account Private Integration Token
//   GHL_INTAKE_PIPELINE_ID — "Inbound Plan Requests" pipeline id  (fill after GHL build)
//   GHL_INTAKE_STAGE_NEW   — "New Request" stage id                (fill after GHL build)
//   GHL_CF_*               — custom field ids (fill after GHL build); optional — if a
//                            field id env var is missing that field is simply skipped.

const GHL_LOCATION_ID = 'cbDr5Xe384SCZnhPMvuZ';
const GHL_BASE = 'https://services.leadconnectorhq.com';

// "Inbound Plan Requests" pipeline — created 2026-05-22. Stable IDs.
const PIPELINE_ID = 'licRJlgNiO90sp0J2A0u';
const STAGE_NEW_REQUEST = 'cb0d5d81-aa42-4240-bdf2-01adf9144a0f';

// Map env-var name -> the request body key it carries.
const CUSTOM_FIELD_ENV = {
  GHL_CF_WEBSITE_URL:               'website_url',
  GHL_CF_PRIMARY_NEED:              'primary_need',
  GHL_CF_MARKETING_COMFORT:         'monthly_marketing_comfort',
  GHL_CF_INTAKE_MESSAGE:            'message',
  GHL_CF_VERTICAL:                  'vertical',
  GHL_CF_UTM_SOURCE:                'utm_source',
  GHL_CF_UTM_MEDIUM:                'utm_medium',
  GHL_CF_UTM_CAMPAIGN:              'utm_campaign',
  GHL_CF_UTM_CONTENT:               'utm_content',
  GHL_CF_GCLID:                     'gclid',
};

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

function toE164(raw) {
  if (!raw) return '';
  const d = String(raw).replace(/\D/g, '');
  if (d.length === 10) return '+1' + d;
  if (d.length === 11 && d[0] === '1') return '+' + d;
  return raw; // leave as-is; GHL will reject silently if invalid
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
    console.log('Honeypot triggered — dropping submission');
    return res.status(200).json({ ok: true });
  }

  // Required fields
  const { full_name, business_name, phone, email } = b;
  if (!full_name || !business_name || !phone || !email) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  const GHL_API_KEY = process.env.GHL_API_KEY;
  if (!GHL_API_KEY) {
    console.error('GHL_API_KEY not configured');
    return res.status(200).json({ ok: true, warning: 'Lead captured pending config' });
  }

  const { firstName, lastName } = splitName(full_name);

  // Build customFields array from whatever env-mapped ids are present.
  const customFields = [];
  for (const [envName, bodyKey] of Object.entries(CUSTOM_FIELD_ENV)) {
    const fieldId = process.env[envName];
    const value = b[bodyKey];
    if (fieldId && value != null && String(value).trim() !== '') {
      customFields.push({ id: fieldId, value: String(value) });
    }
  }

  try {
    // 2. Upsert contact (upsert avoids duplicates on repeat submits).
    const upsertRes = await fetch(GHL_BASE + '/contacts/upsert', {
      method: 'POST',
      headers: ghlHeaders(GHL_API_KEY),
      body: JSON.stringify({
        locationId: GHL_LOCATION_ID,
        firstName,
        lastName,
        name: full_name,
        email,
        phone: toE164(phone),
        companyName: business_name,
        source: 'Growth Plan Intake',
        tags: ['growth-plan-intake', 'inbound-lead'],
        customFields,
      }),
    });
    const upsertData = await upsertRes.json();
    console.log('GHL upsert:', upsertRes.status, JSON.stringify(upsertData).slice(0, 200));

    const contactId =
      (upsertData.contact && upsertData.contact.id) || upsertData.id || null;

    // 3. Create the opportunity in the Inbound Plan Requests pipeline.
    if (contactId) {
      const oppRes = await fetch(GHL_BASE + '/opportunities/', {
        method: 'POST',
        headers: ghlHeaders(GHL_API_KEY),
        body: JSON.stringify({
          pipelineId: PIPELINE_ID,
          locationId: GHL_LOCATION_ID,
          pipelineStageId: STAGE_NEW_REQUEST,
          name: business_name + ' — Inbound',
          status: 'open',
          contactId,
        }),
      });
      console.log('GHL opportunity:', oppRes.status);
      if (!oppRes.ok) {
        console.error('Opportunity create failed:', await oppRes.text());
      }
    } else {
      console.warn('No contactId returned — opportunity skipped');
    }

    return res.status(200).json({ ok: true });
  } catch (err) {
    // Never fail the user — the page should still show its confirmation.
    console.error('submit-intake error:', err && err.message);
    return res.status(200).json({ ok: true, warning: 'Captured with exception' });
  }
}
