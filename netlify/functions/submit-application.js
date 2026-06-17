const { Resend } = require('resend');

const resend = new Resend(process.env.RESEND_API_KEY);

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    const { firstName, lastName, email, age, position, country, message } = JSON.parse(event.body);

    await resend.emails.send({
      from: 'TNL Website <onboarding@resend.dev>',
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

    return {
      statusCode: 200,
      body: JSON.stringify({ success: true })
    };
  } catch (err) {
    console.error('Email send failed:', err.message);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: err.message })
    };
  }
};
