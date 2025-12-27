const mongoose = require("mongoose");

const userSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  password: { type: String, required: false }, // Optional for Google OAuth users
  googleId: { type: String, required: false, unique: true, sparse: true }, // For Google OAuth
  authProvider: { type: String, enum: ['local', 'google'], default: 'local' }
}, { timestamps: true });

module.exports = mongoose.model("User", userSchema);
