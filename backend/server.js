const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { spawn } = require('child_process');

const app = express();
const PORT = 5000;

app.use(cors());
app.use(bodyParser.json());

// POST /recommendations
app.post('/recommendations', (req, res) => {
    // Grab user data from request body
    const userData = req.body;

    const py = spawn('python', ['../ai/scripts/ai_engine.py', '--from_stdin']);


    let output = '';
    let error = '';

    py.stdin.write(JSON.stringify(userData));
    py.stdin.end();

    py.stdout.on('data', (data) => {
        output += data.toString();
    });

    py.stderr.on('data', (data) => {
        error += data.toString();
    });

    py.on('close', (code) => {
        if (code === 0 && output) {
            try {
                // Parse output as JSON (your ai_engine.py should print the final checklist only)
                const jsonStart = output.indexOf('{');
                const jsonStr = output.slice(jsonStart);
                const checklist = JSON.parse(jsonStr);
                res.json(checklist);
            } catch (err) {
                res.status(500).json({ error: "Failed to parse AI output", details: err.message, raw: output });
            }
        } else {
            res.status(500).json({ error: "Python process failed", details: error });
        }
    });
});

app.listen(PORT, () => {
    console.log(`Backend server running on http://localhost:${PORT}`);
});
