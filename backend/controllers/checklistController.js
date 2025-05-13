const { generateChecklist } = require('../ai/generateChecklist');
const Checklist = require('../models/Checklist');

exports.createChecklist = async (req, res) => {
  try {
    const answers = req.body.answers;
    const userId = req.user.id;

    // 1. Generate tasks via AI
    const tasks = await generateChecklist(answers);

    // 2. Save to MongoDB
    const newList = await Checklist.create({
      user: userId,
      items: tasks
    });

    return res.status(201).json(newList);
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: err.message });
  }
};

exports.getChecklist = async (req, res) => {
  try {
    const userId = req.params.id;

    // Fetch the most recent checklist for this user
    const list = await Checklist.findOne({ user: userId }).sort({ createdAt: -1 });
    if (!list) {
      return res.json({ user: userId, items: [] });
    }
    return res.json(list);
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: err.message });
  }
};

// Toggle a single checklist item’s completed status
// @route   PATCH /api/checklist/:listId/items/:itemId
// @access  Private
exports.updateChecklistItem = async (req, res) => {
  try {
    const { listId, itemId } = req.params;
    const { completed } = req.body;

    // 1. Find the checklist document
    const checklist = await Checklist.findById(listId);
    if (!checklist) {
      return res.status(404).json({ message: 'Checklist not found' });
    }

    // 2. Find the sub-item
    const item = checklist.items.id(itemId);
    if (!item) {
      return res.status(404).json({ message: 'Item not found' });
    }

    // 3. Update and save
    item.completed = completed;
    await checklist.save();

    // 4. Return the updated item
    return res.json(item);
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: err.message });
  }
};
