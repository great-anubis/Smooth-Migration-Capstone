const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { spawn } = require('child_process');

const app = express();
const servicesRoute = require('./routes/services');
const PORT = 5000;

app.use(cors());
app.use(bodyParser.json());
app.use(express.json());
app.use('/services', servicesRoute);

app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization');
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    next();
  });
  

// POST /recommendations
app.post('/recommendations', (req, res) => {
    const userData = req.body;
    console.log("📥 Received userData:", userData);

    const py = spawn('python', ['../ai/scripts/ai_engine.py', '--from_stdin']);
    let output = '';
    let error = '';

    py.stdin.write(JSON.stringify(userData));
    py.stdin.end();

    py.stdout.on('data', (data) => {
        output += data.toString();
        console.log("🐍 Python stdout:", data.toString());
    });

    py.stderr.on('data', (data) => {
        error += data.toString();
        console.error("🐍 Python stderr:", data.toString());
    });

    py.on('close', (code) => {
        if (code === 0 && output.trim()) {
            try {
                const jsonStart = output.indexOf('{');
                const jsonStr = output.slice(jsonStart);
                const checklist = JSON.parse(jsonStr);
                res.json(checklist);
            } catch (err) {
                console.error("❌ JSON Parse Error:", err.message);
                res.status(500).json({
                    error: "Failed to parse AI output",
                    details: err.message,
                    raw: output
                });
            }
        } else {
            console.error("❌ Python process failed or empty output");
            res.status(500).json({
                error: "Python process failed",
                details: error || "No output from Python"
            });
        }
    });
});

app.listen(PORT, () => {
    console.log(`🚀 Backend server running on http://localhost:${PORT}`);
});
