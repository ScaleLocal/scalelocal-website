export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const GHL_API_KEY = process.env.GHL_API_KEY;
  const GHL_LOCATION_ID = 'cbDr5Xe384SCZnhPMvuZ';

  try {
    const event = req.body;
    if (event.type !== 'checkout.session.completed') {
      return res.status(200).json({ received: true });
    }

    const session = event.data.object;
    const email = session.customer_details?.email || session.customer_email || '';
    const name = session.customer_details?.name || '';
    const clientRef = session.client_reference_id || '';
    const amountTotal = (session.amount_total || 0) / 100;

    // Parse client_reference_id: "firstName|lastName|phone|businessName|plan|term"
    const parts = clientRef.split('|');
    const firstName = parts[0] || name.split(' ')[0] || '';
    const lastName = parts[1] || name.split(' ').slice(1).join(' ') || '';
    const phone = parts[2] || '';
    const businessName = parts[3] || '';
    const plan = parts[4] || '';
    const term = parts[5] || '';

    // Build tags based on plan and payment context
    const tags = ['payment-received'];

    // Plan tags
    if (plan === 'starter') tags.push('starter-client');
    else if (plan === 'foundation') tags.push('foundation-client');
    else if (plan === 'momentum') tags.push('momentum-client');
    else if (plan === 'authority') tags.push('authority-client');

    // Commitment tags
    if (term === 'nc') tags.push('commitment-m2m');
    else if (term === '6m') tags.push('commitment-6mo');
    else if (term === '12m') tags.push('commitment-12mo');

    // Standalone product detection by amount (when no plan)
    if (!plan || plan === 'none') {
      if (amountTotal === 69) tags.push('deep-audit-paid', 'audit-upgrade-69');
      else if (amountTotal === 97) tags.push('deep-audit-paid');
      else if (amountTotal === 497) tags.push('checkout-paid');
      else if (amountTotal === 500) tags.push('sendlocal-client');
      else if (amountTotal === 1494) tags.push('receptionist-client'); // $997 setup + $497 first month
    }

    // Receptionist detection for bundles
    if (plan === 'momentum' && amountTotal > 2000) tags.push('receptionist-client');
    if (plan === 'authority') tags.push('receptionist-client');

    console.log(`Stripe webhook: ${email}, plan=${plan}, term=${term}, amount=$${amountTotal}, tags=${tags.join(',')}`);

    if (!email && !phone) {
      return res.status(200).json({ received: true, warning: 'no_contact_info' });
    }

    // Find or create GHL contact
    let contactId = null;
    if (email) {
      const searchRes = await fetch(
        `https://services.leadconnectorhq.com/contacts/search/duplicate?locationId=${GHL_LOCATION_ID}&email=${encodeURIComponent(email)}`,
        { headers: { 'Authorization': 'Bearer ' + GHL_API_KEY, 'Version': '2021-07-28' } }
      );
      const searchData = await searchRes.json();
      contactId = searchData.contact?.id;
    }

    if (contactId) {
      // Update existing contact with tags
      await fetch(`https://services.leadconnectorhq.com/contacts/${contactId}`, {
        method: 'PUT',
        headers: { 'Authorization': 'Bearer ' + GHL_API_KEY, 'Version': '2021-07-28', 'Content-Type': 'application/json' },
        body: JSON.stringify({ tags: tags })
      });
    } else {
      // Create new contact
      const createRes = await fetch('https://services.leadconnectorhq.com/contacts/', {
        method: 'POST',
        headers: { 'Authorization': 'Bearer ' + GHL_API_KEY, 'Version': '2021-07-28', 'Content-Type': 'application/json' },
        body: JSON.stringify({
          locationId: GHL_LOCATION_ID,
          firstName: firstName,
          lastName: lastName,
          email: email,
          phone: phone,
          companyName: businessName,
          source: 'Stripe Checkout',
          tags: tags
        })
      });
      const createData = await createRes.json();
      contactId = createData.contact?.id;
    }

    // Internal notification to Matt
    if (contactId) {
      const note = `Payment received: $${amountTotal} | ${firstName} ${lastName} | ${businessName} | Plan: ${plan || 'standalone'} | Term: ${term || 'one-time'} | Tags: ${tags.join(', ')}`;
      await fetch(`https://services.leadconnectorhq.com/contacts/${contactId}/notes`, {
        method: 'POST',
        headers: { 'Authorization': 'Bearer ' + GHL_API_KEY, 'Version': '2021-07-28', 'Content-Type': 'application/json' },
        body: JSON.stringify({ body: note })
      }).catch(() => {});
    }

    return res.status(200).json({ received: true });
  } catch (err) {
    console.error('Webhook error:', err.message);
    return res.status(200).json({ received: true, error: err.message });
  }
}
