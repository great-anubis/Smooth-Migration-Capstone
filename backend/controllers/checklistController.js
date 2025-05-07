const { generateChecklist } = require('../ai/generateChecklist');
const Checklist = require('../models/Checklist');

exports.createChecklist = async (req, res) => {
  try {
    const answers = req.body.answers;
    const userId  = req.user.id;

    // 1. Generate tasks via AI
    const tasks = await generateChecklist(answers);

    // 2. Save to MongoDB
    const newList = await Checklist.create({
      user:  userId,
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
