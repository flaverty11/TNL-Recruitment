const { Resend } = require('resend');

const resend = new Resend(process.env.RESEND_API_KEY);

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  try {
    const { firstName, lastName, email, age, position, country, message } = req.body;

    await resend.emails.send({
      from: 'TNL Website <noreply@tnlrecruitment.com>',
      to: 'tnlrecruitment@outlook.com',
      replyTo: email,
      subject: `New Application — ${firstName} ${lastName}`,
      text: `
New scholarship application from The Next Level website:

Name: ${firstName} ${lastName}
Email: ${email}
Age: ${age}
Position: ${position}
Country: ${country}

Message:
${message || '(none provided)'}
      `.trim()
    });

    return res.status(200).json({ success: true });
  } catch (err) {
    console.error('Email send failed:', err.message);
    return res.status(500).json({ error: err.message });
  }
};
