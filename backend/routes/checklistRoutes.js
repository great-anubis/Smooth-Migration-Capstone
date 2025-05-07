const express = require('express');
const router = express.Router();
const authMiddleware = require('../middlewares/authMiddleware');
const {
  createChecklist,
  getChecklist
} = require('../controllers/checklistController');

// POST /api/checklist/recommendations
router.post(
  '/recommendations',
  authMiddleware,
  createChecklist
);

// GET /api/checklist/user/:id/checklist
router.get(
  '/user/:id/checklist',
  authMiddleware,
  getChecklist
);

module.exports = router;
