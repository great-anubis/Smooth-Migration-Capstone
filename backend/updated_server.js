const express    = require('express');
const cors       = require('cors');
const bodyParser = require('body-parser');
const { spawn }  = require('child_process');


const checklistMapping = require('./models/checklist_mapping.json');

const DUE_DATE_RULES = {
  visa:         14,
  housing:       7,
  job:           7,
  finance:       5,
  legal:        10,
  healthcare:    7,
  post_arrival:  3
};

const app  = express();
const PORT = 5000;

app.use(cors());            
app.use(bodyParser.json()); 


app.post('/recommendations', (req, res, next) => {
  const userData = req.body;
  const py = spawn('python', ['../ai/scripts/ai_engine.py', '--from_stdin']);

  let stdout = '', stderr = '';
  py.stdin.write(JSON.stringify(userData));
  py.stdin.end();

  py.stdout.on('data', d => stdout += d.toString());
  py.stderr.on('data', d => stderr += d.toString());

  py.on('close', code => {
    if (code !== 0) {
      return next(new Error(`Python exited ${code}: ${stderr}`));
    }

    try {
      
      const jsonStart = stdout.indexOf('{');
      const aiResult  = JSON.parse(stdout.slice(jsonStart));
      let tasks       = aiResult.tasks || [];

      
      tasks = tasks.map(task => {
        const text = (task.description || '').toLowerCase();

        
        if (!task.api_trigger) {
          for (const [trigger, keywords] of Object.entries(checklistMapping)) {
            if (keywords.some(kw => text.includes(kw))) {
              task.api_trigger = trigger;
              break;
            }
          }
        }

        
        if (task.api_trigger) {
          task.service = task.api_trigger;
        }

        
        if (!task.due_date && task.api_trigger && DUE_DATE_RULES[task.api_trigger]) {
          const days = DUE_DATE_RULES[task.api_trigger];
          const due  = new Date(Date.now() + days * 86400000);
          task.due_date = due.toISOString().split('T')[0];
        }

        return task;
      });

      res.json({ tasks });
    } catch (err) {
      next(new Error(`Failed to parse/enrich AI output: ${err.message}`));
    }
  });
});


app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({ error: err.message });
});

app.listen(PORT, () => {
  console.log(`🚀 Backend server running on http://localhost:${PORT}`);
});

