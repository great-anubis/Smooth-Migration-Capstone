const mongoose = require('mongoose');

const ChecklistItemSchema = new mongoose.Schema({
  task: { type: String, required: true },
  phase: { type: String, required: true },
  api_trigger: { type: String, default: 'unknown' },
  due_date: { type: Date, default: null },
  completed: { type: Boolean, default: false }
});

const ChecklistSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  migrationProfileId: { type: mongoose.Schema.Types.ObjectId, ref: 'MigrationProfile' },
  items: [ChecklistItemSchema],
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Checklist', ChecklistSchema);
