const User = require("../models/User");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const { OAuth2Client } = require("google-auth-library");

// Initialize Google OAuth2 client
const googleClient = new OAuth2Client(process.env.GOOGLE_CLIENT_ID);

/* ================= REGISTER ================= */
exports.register = async (req, res) => {
  try {
    const { name, email, password } = req.body;

    // 1. user already exists?
    const userExists = await User.findOne({ email });
    if (userExists) {
      return res.status(400).json({ message: "User already exists" });
    }

    // 2. hash password
    const hashedPassword = await bcrypt.hash(password, 10);

    // 3. create user
    const user = await User.create({
      name,
      email,
      password: hashedPassword,
      authProvider: 'local'
    });

    // 4. generate token (AUTO LOGIN)
    const token = jwt.sign(
      { id: user._id },
      process.env.JWT_SECRET,
      { expiresIn: "1d" }
    );

    // 5. send token + name
    res.status(201).json({
      token,
      name: user.name
    });

  } catch (err) {
    res.status(500).json({ message: "Server error" });
  }
};

/* ================= LOGIN ================= */
exports.login = async (req, res) => {
  try {
    const { email, password } = req.body;

    const user = await User.findOne({ email });
    if (!user) {
      return res.status(400).json({ message: "Invalid credentials" });
    }

    // Check if user registered via Google OAuth
    if (user.authProvider === 'google' && !user.password) {
      return res.status(400).json({
        message: "This account was created with Google. Please use Google Sign-In."
      });
    }

    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) {
      return res.status(400).json({ message: "Invalid credentials" });
    }

    const token = jwt.sign(
      { id: user._id },
      process.env.JWT_SECRET,
      { expiresIn: "1d" }
    );

    res.json({
      token,
      name: user.name
    });

  } catch (err) {
    res.status(500).json({ message: "Server error" });
  }
};

/* ================= GOOGLE LOGIN ================= */
exports.googleLogin = async (req, res) => {
  try {
    const { credential } = req.body;

    if (!credential) {
      return res.status(400).json({ message: "Google credential is required" });
    }

    // Verify the Google ID token
    const ticket = await googleClient.verifyIdToken({
      idToken: credential,
      audience: process.env.GOOGLE_CLIENT_ID
    });

    const payload = ticket.getPayload();
    const { sub: googleId, email, name, picture } = payload;

    // Check if user exists with this Google ID or email
    let user = await User.findOne({
      $or: [{ googleId }, { email }]
    });

    if (user) {
      // User exists - update Google ID if not set
      if (!user.googleId) {
        user.googleId = googleId;
        user.authProvider = 'google';
        await user.save();
      }
    } else {
      // Create new user with Google credentials
      user = await User.create({
        name,
        email,
        googleId,
        authProvider: 'google'
        // No password required for Google OAuth users
      });
    }

    // Generate JWT token
    const token = jwt.sign(
      { id: user._id },
      process.env.JWT_SECRET,
      { expiresIn: "1d" }
    );

    res.json({
      token,
      name: user.name,
      email: user.email,
      picture // Optional: return profile picture
    });

  } catch (err) {
    console.error("Google login error:", err);
    res.status(500).json({ message: "Google authentication failed" });
  }
};
