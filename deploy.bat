@echo off
REM ============================================================
REM  deploy.bat  -  One-click deploy for scalelocal.net
REM  Double-click this any time to publish your changes:
REM    stage -> commit -> pull (rebase) -> push -> Vercel deploys.
REM  Runs git on YOUR machine with YOUR credentials.
REM ============================================================
setlocal enabledelayedexpansion
cd /d "%~dp0"

REM --- optional commit message: pass as argument, else timestamped ---
set "MSG=%~1"
if "%MSG%"=="" (
  for /f "tokens=2 delims==" %%a in ('wmic os get localdatetime /value 2^>nul') do set "DT=%%a"
  set "STAMP=!DT:~0,4!-!DT:~4,2!-!DT:~6,2! !DT:~8,2!:!DT:~10,2!"
  set "MSG=site update !STAMP!"
)

echo.
echo ============================================================
echo  Deploying scalelocal.net
echo  Commit message: !MSG!
echo ============================================================

echo.
echo [1/4] Staging changes...
git add -A

echo.
echo [2/4] Committing...
git commit -m "!MSG!"
if errorlevel 1 (
  echo   Nothing new to commit, or commit failed - continuing to sync anyway.
)

echo.
echo [3/4] Syncing with GitHub (rebase, auto-resolve unrelated conflicts to remote)...
git pull --rebase --autostash -X theirs
if errorlevel 1 (
  echo.
  echo  !! Sync hit a snag. Send the messages above to Claude. Stopping so nothing breaks.
  pause
  exit /b 1
)

echo.
echo [4/4] Pushing to GitHub...
git push
if errorlevel 1 (
  echo.
  echo  !! Push failed - scroll up for the reason - often a one-time login -. Send it to Claude.
  pause
  exit /b 1
)

echo.
echo ============================================================
echo  SUCCESS - pushed to GitHub. Vercel auto-deploys in ~1-2 min.
echo  Live at: https:^/^/www.scalelocal.net
echo ============================================================
echo.
pause
