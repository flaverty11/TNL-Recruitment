const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  try {
    const { productKey, amountPence, productName } = req.body;

    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [{
        price_data: {
          currency: 'gbp',
          product_data: { name: productName },
          unit_amount: amountPence,
        },
        quantity: 1,
      }],
      mode: 'payment',
      success_url: 'https://www.tnlrecruitment.com/coach-contacts.html?payment=success',
      cancel_url: 'https://www.tnlrecruitment.com/coach-contacts.html?payment=cancelled',
      metadata: { productKey },
      customer_creation: 'always',
    });

    return res.status(200).json({ url: session.url });
  } catch (err) {
    return res.status(400).json({ error: err.message });
  }
}
