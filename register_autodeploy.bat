@echo off
REM One-time setup. Registers BOTH scheduled tasks to run completely hidden -
REM no console window will ever flash on your screen.
setlocal
set "HERE=%~dp0"

echo Registering auto-deploy watcher - runs every 5 minutes, silently...
schtasks /Create /TN "ScaleLocal AutoDeploy" /TR "wscript.exe \"%HERE%autodeploy_silent.vbs\"" /SC MINUTE /MO 5 /F

echo.
echo Re-registering the daily article publisher to run silently too...
schtasks /Create /TN "ScaleLocal Daily Article" /TR "wscript.exe \"%HERE%publish_silent.vbs\"" /SC DAILY /ST 09:00 /RL HIGHEST /F

echo.
echo ============================================================
echo  Both tasks registered. Neither will ever show a window.
echo.
echo  AutoDeploy stays idle unless _deploy_request.txt exists,
echo  and only ever stages the exact paths listed inside it.
echo.
echo  Watch it:   type _published_log\autodeploy.log
echo  Run now:    schtasks /Run /TN "ScaleLocal AutoDeploy"
echo  Pause it:   schtasks /Change /TN "ScaleLocal AutoDeploy" /DISABLE
echo  Remove it:  schtasks /Delete /TN "ScaleLocal AutoDeploy" /F
echo ============================================================
echo.
pause
