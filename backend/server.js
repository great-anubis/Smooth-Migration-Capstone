const express    = require('express');
const cors       = require('cors');
const bodyParser = require('body-parser');
const { spawn }  = require('child_process');

const checklistMapping = require('./models/checklist_mapping.json');
const { checklistSchema } = require('./validation/checklistSchema');

const DUE_DATE_RULES = {
  visa:14, housing:7, job:7, finance:5,
  legal:10, healthcare:7, post_arrival:3
};

const app = express();
app.use(cors());
app.use(bodyParser.json());

app.post('/recommendations', (req, res, next) => {
  const py = spawn('python', ['../ai/scripts/ai_engine.py','--from_stdin']);
  py.stdin.write(JSON.stringify(req.body));
  py.stdin.end();

  let out='', err='';
  py.stdout.on('data', d=> out+=d);
  py.stderr.on('data', d=> err+=d);

  py.on('close', code => {
    if(code!==0) return next(new Error(`AI error: ${err}`));
    try {
      const jsonStart = out.indexOf('{');
      const aiRes     = JSON.parse(out.slice(jsonStart));
      const { error } = checklistSchema.validate(aiRes,{abortEarly:false});
      if(error) return res.status(400).json({ validationErrors:error.details });

      const tasks = aiRes.tasks.map(task=>{
        const text = (task.description||'').toLowerCase().replace(/[^\w\s]/g,' ');
        if(!task.api_trigger){
          task.api_trigger = Object.entries(checklistMapping)
            .find(([t,kws])=> kws.some(kw=> text.includes(kw)))?.[0] || 'general';
        }
        task.service = task.api_trigger;
        if(!task.due_date && DUE_DATE_RULES[task.api_trigger]){
          const d = new Date(Date.now()+DUE_DATE_RULES[task.api_trigger]*86400000);
          task.due_date = d.toISOString().split('T')[0];
        }
        return task;
      });

      res.json({ tasks });
    } catch(e){
      next(new Error(`Parse/enrich error: ${e.message}`));
    }
  });
});


app.use((err,req,res,next)=>{
  console.error(err);
  res.status(500).json({ error:err.message });
});

app.listen(5000, () => console.log(' Backend server on http://localhost:5000'));


