@echo off
:: Discord Audio Archive Bot - Windows Background Service
:: =====================================================
:: Runs the hybrid bot as a background process with automatic restart
:: Optimized for minimal resource usage and maximum reliability

title Discord Audio Archive Bot

:: Set environment variables for background operation
set BACKGROUND_MODE=true
set NODE_ENV=production

:: Check if we're running as Administrator (for service creation)
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] Running with Administrator privileges - Service mode available
    set ADMIN_MODE=true
) else (
    echo [INFO] Running in user mode
    set ADMIN_MODE=false
)

echo.
echo =====================================================
echo   Discord Audio Archive Bot - Windows Service
echo =====================================================
echo.
echo [INFO] Starting background service...
echo [INFO] Process will restart automatically on failure
echo [INFO] Press Ctrl+C to stop the service
echo.

:: Create log file with timestamp
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "fullstamp=%YYYY%-%MM%-%DD%_%HH%-%Min%-%Sec%"
set LOG_FILE=logs\bot_%fullstamp%.log

:: Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

echo [%date% %time%] Bot service started > "%LOG_FILE%"

:: Main service loop
:service_loop

:: Check if venv exists, create if needed
if not exist "venv" (
    echo [INFO] Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        echo [ERROR] Please ensure Python 3.8+ is installed
        pause
        exit /b 1
    )
)

:: Activate virtual environment and install dependencies
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

:: Check if requirements are installed
python -c "import discord" 2>nul
if errorlevel 1 (
    echo [INFO] Installing Python dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install Python dependencies
        pause
        exit /b 1
    )
)

:: Check Node.js dependencies
if not exist "node_modules" (
    echo [INFO] Installing Node.js dependencies...
    npm install
    if errorlevel 1 (
        echo [ERROR] Failed to install Node.js dependencies
        pause
        exit /b 1
    )
)

:: Check configuration
if not exist ".env" (
    echo [ERROR] Configuration file .env not found
    echo [INFO] Please copy .env.example to .env and configure your settings
    pause
    exit /b 1
)

:: Memory and resource optimization for Windows
set NODE_OPTIONS=--max-old-space-size=128 --gc-interval=100

:: Set process priority to low for background operation
wmic process where name="python.exe" CALL setpriority "below normal" >nul 2>&1
wmic process where name="node.exe" CALL setpriority "below normal" >nul 2>&1

echo [%date% %time%] Starting hybrid bot components... >> "%LOG_FILE%"
echo [INFO] Starting hybrid bot components...

:: Start the hybrid bot system with restart logic
:restart_loop

:: Clean up any existing processes
taskkill /f /im python.exe /fi "WindowTitle eq Discord Audio Archive Bot*" >nul 2>&1
taskkill /f /im node.exe /fi "WindowTitle eq Discord Audio Archive Bot*" >nul 2>&1

:: Start Node.js voice recorder in background
echo [INFO] Starting Node.js voice recorder...
start /B /MIN "Discord Audio Archive Bot - Voice Recorder" node voice_recorder.js

:: Wait for Node.js to initialize
timeout /t 3 /nobreak >nul

:: Start Python bot
echo [INFO] Starting Python event monitor...
python hybrid_bot.py

:: If we get here, the Python bot has stopped
set EXIT_CODE=%errorlevel%
echo [%date% %time%] Python bot stopped with exit code %EXIT_CODE% >> "%LOG_FILE%"

:: Check exit code and decide whether to restart
if %EXIT_CODE% equ 0 (
    echo [INFO] Bot stopped normally
    goto end_service
) else (
    echo [WARNING] Bot stopped with error code %EXIT_CODE%
    echo [INFO] Restarting in 10 seconds...
    echo [%date% %time%] Restarting due to error... >> "%LOG_FILE%"

    :: Clean up Node.js process before restart
    taskkill /f /im node.exe /fi "WindowTitle eq Discord Audio Archive Bot*" >nul 2>&1

    timeout /t 10 /nobreak
    goto restart_loop
)

:end_service
echo [%date% %time%] Service stopped >> "%LOG_FILE%"
echo [INFO] Discord Audio Archive Bot service stopped

:: Clean up background processes
taskkill /f /im node.exe /fi "WindowTitle eq Discord Audio Archive Bot*" >nul 2>&1

if "%ADMIN_MODE%"=="true" (
    echo.
    echo [INFO] To install as Windows Service, run:
    echo [INFO] powershell -ExecutionPolicy Bypass -File install_windows_service.ps1
)

echo.
echo [INFO] Thank you for using Discord Audio Archive Bot!
pause
