import admin from 'firebase-admin';

// Initialize Firebase only once
if (!admin.apps.length) {
  admin.initializeApp({
    credential: admin.credential.cert({
      projectId: process.env.FIREBASE_PROJECT_ID,
      clientEmail: process.env.FIREBASE_CLIENT_EMAIL,
      // We replace escaped newlines so the key works in Vercel
      privateKey: process.env.FIREBASE_PRIVATE_KEY.replace(/\\n/g, '\n'),
    }),
  });
}

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).send('Use POST');

  const { deviceToken } = req.body; // Sent from YOLO script

  const message = {
    notification: {
      title: '🔥 FIRE DETECTED!',
      body: 'Emergency: Fire detected at the camera location.',
    },
    token: deviceToken, // This is your Flutter app's unique ID
  };

  try {
    await admin.messaging().send(message);
    return res.status(200).json({ success: true });
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
}