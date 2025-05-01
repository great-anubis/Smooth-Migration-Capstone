const express = require('express');
const router = express.Router();
const fs = require('fs');
const path = require('path');

// GET /services/:trigger
router.get('/:trigger', (req, res) => {
  const trigger = req.params.trigger;

  const filePath = path.join(__dirname, '../data/checklist_mapping.json');
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      return res.status(500).json({ error: 'Failed to read mapping file' });
    }

    let mapping;
    try {
      mapping = JSON.parse(data);
    } catch (parseErr) {
      return res.status(500).json({ error: 'Invalid JSON in mapping file' });
    }

    const service = mapping[trigger];
    if (!service) {
      return res.status(404).json({ error: 'No service found for this trigger' });
    }

    return res.json(service);
  });
});

module.exports = router;
