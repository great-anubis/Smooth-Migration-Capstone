@echo off
REM Activate the virtual environment
call ..\env\Scripts\activate.bat

REM Run the baseline model script
python ..\models\baseline_model.py

pause
