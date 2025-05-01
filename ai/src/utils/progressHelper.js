function calculateChecklistProgress(checklist) {
    if (!Array.isArray(checklist) || checklist.length === 0) return 0;
  
    const completedCount = checklist.filter(task => task.completed).length;
    const progress = (completedCount / checklist.length) * 100;
  
    return Math.round(progress);
  }
  
  module.exports = { calculateChecklistProgress };  