const mongoose = require('mongoose');

const checklistSchema = new mongoose.Schema({
  user: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  title: String,
  tasks: [String],
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Checklist', checklistSchema);
