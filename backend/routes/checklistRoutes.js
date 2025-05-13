const express = require('express');
const router = express.Router();
const authMiddleware = require('../middlewares/authMiddleware');
const {
  createChecklist,
  getChecklist,
  updateChecklistItem
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

// PATCH /api/checklist/:listId/items/:itemId
router.patch(
  '/:listId/items/:itemId',
  authMiddleware,
  updateChecklistItem
);

module.exports = router;