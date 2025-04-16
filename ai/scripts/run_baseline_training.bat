@echo off
REM Activate the virtual environment
echo Activating virtual environment...
call ..\env\Scripts\activate

REM Navigate to the AI root folder (if necessary)
cd /d %~dp0..\

REM Run the baseline model script and output its JSON result
echo Running baseline model test...
python models\baseline_model.py

REM Validate checklist mapping
echo Validating checklist mapping...
python scripts\validate_mapping.py

REM (Optional) Remind the user to run the Flask API stub in a separate window for integration testing
echo Please ensure your Flask API stub is running for integration tests.
pause
