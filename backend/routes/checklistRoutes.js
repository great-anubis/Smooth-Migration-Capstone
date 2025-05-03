const express = require('express');
const {
  createChecklist,
  getChecklists,
  deleteChecklist
} = require('../controllers/checklistController');
const auth = require('../middlewares/authMiddleware');

const router = express.Router();

router.post('/', auth, createChecklist);
router.get('/', auth, getChecklists);
router.delete('/:id', auth, deleteChecklist);

module.exports = router;
