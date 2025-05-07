// backend/models/Checklist.js
const mongoose = require('mongoose');

const ChecklistItemSchema = new mongoose.Schema({
  task:      { type: String, required: true },
  dueDate:   { type: Date,   default: null },
  completed: { type: Boolean, default: false }
});

const ChecklistSchema = new mongoose.Schema({
  user:  { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  items: [ChecklistItemSchema],
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Checklist', ChecklistSchema);
