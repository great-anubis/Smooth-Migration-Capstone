const Checklist = require('../models/Checklist');

exports.createChecklist = async (req, res) => {
  const { title, tasks } = req.body;
  try {
    const checklist = await Checklist.create({
      user: req.user.id,
      title,
      tasks
    });
    res.status(201).json(checklist);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
};

exports.getChecklists = async (req, res) => {
  try {
    const lists = await Checklist.find({ user: req.user.id });
    res.json(lists);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

exports.deleteChecklist = async (req, res) => {
  try {
    await Checklist.findByIdAndDelete(req.params.id);
    res.json({ message: 'Checklist deleted' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};
