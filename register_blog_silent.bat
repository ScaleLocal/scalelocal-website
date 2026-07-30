@echo off
REM ============================================================
REM  RUN THIS ONE FROM AN **ADMIN** COMMAND PROMPT.
REM
REM  The existing "ScaleLocal Daily Article" task was created with /RL HIGHEST
REM  (run with highest privileges), so replacing it requires elevation - that is
REM  why a normal prompt returns "ERROR: Access is denied."
REM
REM  This only changes HOW it launches - hidden, via publish_silent.vbs.
REM  The 9:00 AM schedule and /RL HIGHEST are preserved exactly.
REM ============================================================
setlocal
set "HERE=%~dp0"

net session >nul 2>&1
if errorlevel 1 goto :notadmin

schtasks /Create /TN "ScaleLocal Daily Article" /TR "wscript.exe \"%HERE%publish_silent.vbs\"" /SC DAILY /ST 09:00 /RL HIGHEST /F
echo.
echo Done - the 9:00 AM publisher will no longer show a window.
echo Re-check the wake/missed-run boxes in Task Scheduler if they were set.
echo.
pause
goto :eof

:notadmin
echo.
echo   This window is NOT elevated.
echo   Close it, right-click Command Prompt, choose "Run as administrator",
echo   then run this file again.
echo.
pause
