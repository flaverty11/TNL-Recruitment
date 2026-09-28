// Netlify wrapper around the shared handler in api/submit-application.js (used by Vercel).
const handler = require('../../api/submit-application.js');

exports.handler = async (event) => {
  let body = {};
  try {
    body = JSON.parse(event.body || '{}');
  } catch (err) {
    return { statusCode: 400, body: JSON.stringify({ error: 'Invalid JSON' }) };
  }

  let statusCode = 200;
  let payload = {};
  const res = {
    status(code) { statusCode = code; return res; },
    json(data) { payload = data; return res; },
  };

  await handler({ method: event.httpMethod, body }, res);
  return { statusCode, body: JSON.stringify(payload) };
};
