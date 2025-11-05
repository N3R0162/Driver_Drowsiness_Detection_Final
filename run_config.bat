@echo off
echo ========================================
echo Driver Drowsiness Detection System
echo PERCLOS Configuration Interface
echo ========================================
echo.
echo Starting Streamlit application...
echo Navigate to Configuration page to adjust PERCLOS thresholds
echo.
cd source
streamlit run launcher.py
pause
