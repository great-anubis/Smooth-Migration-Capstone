const Joi = require("joi");

const taskSchema = Joi.object({
  id:          Joi.string().required(),
  description: Joi.string().required(),
  api_trigger: Joi.string().required(),
  service:     Joi.string().required(),
  due_date:    Joi.date().iso().required(),
  completed:   Joi.boolean().required(),
});

const checklistSchema = Joi.object({
  tasks: Joi.array().items(taskSchema).min(1).required(),
});

module.exports = { checklistSchema };
