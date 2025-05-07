/*
File: backend/ai/generateChecklist.js
Purpose: Wrapper to call your existing Python AI engine (ai/scripts/ai_engine.py)
*/

const { spawn } = require('child_process');
const path = require('path');

/**
 * Calls the Python AI engine CLI and returns a flat array of checklist items.
 * @param {Object} answers - Flat key/value pairs of user answers
 * @returns {Promise<Array<{ task: string, phase: string, api_trigger: string, due_date: Date|null, completed: boolean }>>}
 */
async function generateChecklist(answers) {
  return new Promise((resolve, reject) => {
    // Adjust the Python command if needed (e.g., 'py' or 'python3')
    const pythonCmd = 'python';
    const scriptPath = path.resolve(__dirname, '../../ai/scripts/ai_engine.py');
    const proc = spawn(pythonCmd, [scriptPath, '--from_stdin'], { cwd: path.resolve(__dirname, '../../ai/scripts') });

    let stdout = '';
    let stderr = '';

    proc.stdout.on('data', (data) => {
      stdout += data.toString();
    });
    proc.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    proc.on('close', (code) => {
      if (code !== 0) {
        return reject(new Error(`AI engine exited with code ${code}: ${stderr}`));
      }
      try {
        const raw = JSON.parse(stdout);
        // raw is an object with phases as keys -> lists of tasks
        const items = [];
        Object.values(raw).forEach(arr => {
          if (Array.isArray(arr)) {
            arr.forEach(task => items.push(task));
          }
        });
        resolve(items);
      } catch (err) {
        reject(new Error(`Failed to parse AI output: ${err.message}`));
      }
    });

    // Write JSON to stdin
    proc.stdin.write(JSON.stringify(answers));
    proc.stdin.end();
  });
}

module.exports = { generateChecklist };
