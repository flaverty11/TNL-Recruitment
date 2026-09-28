const Stripe = require('stripe');

// Prices are set here on the server. The browser only says which product it wants.
const PRODUCTS = {
  'NCAA Division I':      { name: 'NCAA Division I Coach Contacts',      pence: 9900 },
  'NCAA Division II':     { name: 'NCAA Division II Coach Contacts',     pence: 7900 },
  'NCAA Division III':    { name: 'NCAA Division III Coach Contacts',    pence: 4900 },
  'NAIA Division I':      { name: 'NAIA Division I Coach Contacts',      pence: 7900 },
  'NAIA Division II':     { name: 'NAIA Division II Coach Contacts',     pence: 5900 },
  'NJCAA Junior College': { name: 'NJCAA Junior College Coach Contacts', pence: 4900 },
  'Complete Bundle':      { name: 'Complete Bundle — All Divisions',     pence: 29900 },
};

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const stripe = Stripe(process.env.STRIPE_SECRET_KEY);

  try {
    const { productKey } = req.body || {};
    const product = Object.prototype.hasOwnProperty.call(PRODUCTS, productKey) ? PRODUCTS[productKey] : null;
    if (!product) {
      return res.status(400).json({ error: 'Unknown product' });
    }

    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [{
        price_data: {
          currency: 'gbp',
          product_data: { name: product.name },
          unit_amount: product.pence,
        },
        quantity: 1,
      }],
      mode: 'payment',
      success_url: 'https://www.tnlrecruitment.com/coach-contacts?payment=success',
      cancel_url: 'https://www.tnlrecruitment.com/coach-contacts?payment=cancelled',
      metadata: { productKey },
      customer_creation: 'always',
    });

    return res.status(200).json({ url: session.url });
  } catch (err) {
    console.error('Checkout session failed:', err.message);
    return res.status(500).json({ error: 'Could not start checkout' });
  }
};
