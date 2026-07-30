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
REM    * Stages ONLY the paths listed in that file. Never "git add -A".
REM    * Refuses to run if no paths are listed.
REM    * Unrelated dirty files are shelved by --autostash and put straight back.
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

if not defined MSG (
  call :log "** request file had no commit message - ignoring, left in place"
  goto :eof
)
if %NPATHS%==0 (
  call :log "** request listed NO paths - refusing to deploy. Left in place."
  call :log "   Add one repo-relative path per line after the commit message."
  goto :eof
)

call :log "======== autodeploy start ========"
call :log "message: !MSG!"
call :log "paths staged: %NPATHS%"

git diff --cached --quiet
if not errorlevel 1 (
  call :log "nothing staged from those paths - clearing request, no commit"
  del "%REQ%"
  goto :eof
)

git commit -m "!MSG!" >>"%LOG%" 2>&1
if errorlevel 1 (
  call :log "** COMMIT FAILED - request left in place for retry"
  goto :eof
)

REM --autostash so files you are mid-edit on can never block the rebase
git pull --rebase --autostash -X theirs >>"%LOG%" 2>&1
if errorlevel 1 (
  call :log "** PULL FAILED - refusing to push. Investigate."
  goto :eof
)

git push >>"%LOG%" 2>&1
if errorlevel 1 (
  call :log "** PUSH FAILED - request left in place for retry"
  goto :eof
)

del "%REQ%"
call :log "OK - pushed. Vercel builds in about 1-2 minutes."
call :log "======== autodeploy end ========"
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
