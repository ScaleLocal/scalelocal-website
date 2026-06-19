@echo off
REM ============================================================
REM  daily_publish.bat - ScaleLocal auto-publisher (Task Scheduler)
REM  Publishes ONE queued article/day. Fully unattended.
REM  Needs: PC on + online at run time. Git already authenticated.
REM ============================================================
cd /d "%~dp0"

REM Find python (py launcher preferred, else python on PATH)
where py >nul 2>&1 && ( set "PY=py" ) || ( set "PY=python" )

echo [%date% %time%] daily_publish starting >> "_published_log\runner.log"
%PY% "%~dp0publish_next_article.py" >> "_published_log\runner.log" 2>&1
echo [%date% %time%] daily_publish finished (exit %errorlevel%) >> "_published_log\runner.log"
exit /b 0
