@echo off
REM ============================================================
REM  autodeploy.bat - ScaleLocal unattended deploy watcher
REM
REM  WHY: Claude writes files through the Cowork device bridge, which cannot
REM  unlink. Git needs unlink to write objects and clear .git/index.lock, so
REM  "git add" from that side always stages 0 files. This runs natively on
REM  Windows, where unlink works, and commits+pushes on Claude's behalf.
REM
REM  SAFETY - it does NOT touch anything you are mid-edit on:
REM    * Idle unless _deploy_request.txt exists.
REM    * Stages ONLY the paths listed in that file. Never stages everything.
REM    * Refuses to run if no paths are listed.
REM    * Files you are editing are shelved by --autostash and put straight back.
REM
REM  REQUEST FILE FORMAT
REM    line 1  = commit message
REM    line 2+ = one repo-relative path per line to stage
REM ============================================================
setlocal enabledelayedexpansion
cd /d "%~dp0"

set "REQ=_deploy_request.txt"
set "LOG=_published_log\autodeploy.log"

if not exist "%REQ%" goto :eof
if not exist "_published_log" mkdir "_published_log"

set "MSG="
set /a NPATHS=0

for /f "usebackq delims=" %%L in ("%REQ%") do call :handleline "%%L"

if not defined MSG goto :nomsg
if %NPATHS%==0 goto :nopaths

call :log "======== autodeploy start ========"
call :log "message: !MSG!"
call :log "paths staged: %NPATHS%"

git diff --cached --quiet
if not errorlevel 1 goto :nocommit

git commit -m "!MSG!" >>"%LOG%" 2>&1
if errorlevel 1 goto :commitfail
goto :sync

:nocommit
call :log "no new changes in the listed paths - will still sync any pending commits"

:sync
REM --autostash so files you are mid-edit on can never block the rebase
git pull --rebase --autostash -X theirs >>"%LOG%" 2>&1
if errorlevel 1 goto :pullfail

git push >>"%LOG%" 2>&1
if errorlevel 1 goto :pushfail

del "%REQ%"
call :log "OK - synced and pushed. Vercel builds in about 1-2 minutes."
call :log "======== autodeploy end ========"
goto :eof

:nomsg
call :log "** request file had no commit message - ignoring, left in place"
goto :eof
:nopaths
call :log "** request listed NO paths - refusing to deploy. Left in place."
call :log "   Add one repo-relative path per line after the commit message."
goto :eof
:commitfail
call :log "** COMMIT FAILED - request left in place for retry"
goto :eof
:pullfail
call :log "** PULL FAILED - refusing to push. Investigate."
goto :eof
:pushfail
call :log "** PUSH FAILED - request left in place for retry"
goto :eof

:handleline
set "LINE=%~1"
if "%LINE%"=="" exit /b 0
if not defined MSG (
  set "MSG=%LINE%"
  exit /b 0
)
set /a NPATHS+=1
git add -- "%LINE%" >>"%LOG%" 2>&1
exit /b 0

:log
echo [%date% %time%] %~1 >>"%LOG%"
exit /b 0
