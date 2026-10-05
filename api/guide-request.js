const { Resend } = require('resend');

const resend = new Resend(process.env.RESEND_API_KEY);

const INBOX = 'tnlrecruitment@outlook.com';
const GUIDE_URL = 'https://www.tnlrecruitment.com/downloads/tnl-parent-guide.pdf';
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function field(body, key) {
  const value = body && typeof body[key] === 'string' ? body[key].trim() : '';
  return value.replace(/[\r\n]+/g, ' ').slice(0, 200);
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const name = field(req.body, 'name');
  const email = field(req.body, 'email');
  const role = field(req.body, 'role');

  // Honeypot: real visitors never see the "website" field, bots fill it in.
  if (field(req.body, 'website')) {
    return res.status(200).json({ success: true });
  }

  if (!name || !EMAIL_RE.test(email)) {
    return res.status(400).json({ error: 'Please enter your name and a valid email address.' });
  }

  try {
    await resend.emails.send({
      from: 'The Next Level <noreply@tnlrecruitment.com>',
      to: email,
      replyTo: INBOX,
      subject: 'Your free guide to US soccer scholarships',
      attachments: [{ path: GUIDE_URL, filename: 'TNL-Parent-Guide-US-Soccer-Scholarships.pdf' }],
      text: `
Hi ${name},

Thanks for downloading The UK & Irish Parent's Guide to US Soccer Scholarships. It's attached to this email as a PDF, and you can also open it here:
${GUIDE_URL}

Inside: how US college soccer works, what it really costs, grades and eligibility, a timeline by age, highlight reel tips, and the questions to ask any coach or agency.

When you're ready, our free evaluation tells you honestly where your child stands, with no obligation:
https://www.tnlrecruitment.com/#apply

Or message us on WhatsApp: https://wa.me/447346804838

Best wishes,
The Next Level
https://www.tnlrecruitment.com
      `.trim()
    });
  } catch (err) {
    console.error('Guide email failed:', err.message);
    return res.status(500).json({ error: 'Email send failed' });
  }

  // Lead notification. If this fails the visitor still has their guide.
  try {
    await resend.emails.send({
      from: 'TNL Website <noreply@tnlrecruitment.com>',
      to: INBOX,
      replyTo: email,
      subject: `New guide download — ${name}`,
      text: `
Someone downloaded the free parent guide:

Name: ${name}
Email: ${email}
Who they are: ${role || '(not given)'}

They have NOT applied yet. A friendly follow-up in a few days could help.
      `.trim()
    });
  } catch (err) {
    console.error('Guide lead notification failed:', err.message);
  }

  return res.status(200).json({ success: true });
};
