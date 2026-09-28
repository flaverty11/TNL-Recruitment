const { Resend } = require('resend');

const resend = new Resend(process.env.RESEND_API_KEY);

const INBOX = 'tnlrecruitment@outlook.com';
const REQUIRED = ['firstName', 'lastName', 'email', 'phone', 'age', 'position', 'country', 'club', 'level', 'startTerm'];
const FIELDS = [...REQUIRED, 'video', 'message', 'website'];
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function clean(body) {
  const out = {};
  for (const key of FIELDS) {
    const value = body && typeof body[key] === 'string' ? body[key].trim() : '';
    const max = key === 'message' ? 3000 : 300;
    // Single-line fields must not contain line breaks (they end up in the subject line)
    out[key] = key === 'message' ? value.slice(0, max) : value.replace(/[\r\n]+/g, ' ').slice(0, max);
  }
  return out;
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const f = clean(req.body);

  // Honeypot: real visitors never see the "website" field, bots fill it in.
  // Pretend it worked so the bot moves on.
  if (f.website) {
    return res.status(200).json({ success: true });
  }

  const missing = REQUIRED.filter((key) => !f[key]);
  if (missing.length || !EMAIL_RE.test(f.email)) {
    return res.status(400).json({ error: 'Please fill in all required fields with a valid email address.' });
  }

  try {
    await resend.emails.send({
      from: 'TNL Website <noreply@tnlrecruitment.com>',
      to: INBOX,
      replyTo: f.email,
      subject: `New Application — ${f.firstName} ${f.lastName}`,
      text: `
New scholarship application from The Next Level website:

Name: ${f.firstName} ${f.lastName}
Email: ${f.email}
Phone: ${f.phone}
Age: ${f.age}
Position: ${f.position}
Country: ${f.country}
Club: ${f.club}
Level: ${f.level}
Planned start: ${f.startTerm}
Highlight video: ${f.video || '(not provided)'}

Message:
${f.message || '(none provided)'}
      `.trim()
    });
  } catch (err) {
    console.error('Email send failed:', err.message);
    return res.status(500).json({ error: 'Email send failed' });
  }

  // Confirmation to the applicant. If this fails the application is still received.
  try {
    await resend.emails.send({
      from: 'The Next Level <noreply@tnlrecruitment.com>',
      to: f.email,
      replyTo: INBOX,
      subject: 'We’ve received your application — The Next Level',
      text: `
Hi ${f.firstName},

Thanks for applying to The Next Level. We've received your details and a scholarship advisor will be in touch within 24 hours to arrange your free evaluation call.

To help us prepare, have these ready if you can:
- A highlight video or full-match footage
- Your latest school grades (GCSEs, A-levels, Leaving Cert or equivalent)
- Your current club and the level you play at

Want a quicker reply? Message us on WhatsApp: https://wa.me/447346804838

Speak soon,
The Next Level
https://www.tnlrecruitment.com
      `.trim()
    });
  } catch (err) {
    console.error('Confirmation email failed:', err.message);
  }

  return res.status(200).json({ success: true });
};
