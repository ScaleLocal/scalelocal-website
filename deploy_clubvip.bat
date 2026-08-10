@echo off
REM ============================================================
REM  deploy_clubvip.bat  -  one-off deploy for the Club VIP page
REM
REM  Does what deploy.bat does, plus one extra step first: it stops
REM  tracking the _to_delete\ scratch folder, which `git add -A`
REM  swept into the repo (282 files, ~9 MB) on 2026-08-10.
REM
REM  Nothing is deleted from your disk. `git rm --cached` only tells
REM  git to stop tracking those files; they stay exactly where they are.
REM
REM  Double-click this once. After it succeeds you can go back to
REM  using deploy.bat normally.
REM ============================================================
setlocal
cd /d "%~dp0"

echo.
echo [1/5] Untracking the _to_delete scratch folder...
git rm -r --cached --quiet _to_delete 2>nul
if errorlevel 1 echo   Nothing to untrack - fine, continuing.

echo.
echo [2/5] Staging changes...
git add -A

echo.
echo [3/5] Committing...
git commit -m "Club VIP landing page; stop tracking _to_delete scratch"
if errorlevel 1 echo   Nothing new to commit - continuing to sync anyway.

echo.
echo [4/5] Syncing with GitHub...
git pull --rebase --autostash -X theirs
if errorlevel 1 (
  echo.
  echo  !! Sync hit a snag. Send the messages above to Claude. Stopping.
  pause
  exit /b 1
)

echo.
echo [5/5] Pushing...
git push
if errorlevel 1 (
  echo.
  echo  !! Push failed - scroll up for the reason - and send it to Claude.
  pause
  exit /b 1
)

echo.
echo ============================================================
echo  SUCCESS. Vercel deploys in 1-2 minutes.
echo  Live at: https:^/^/www.scalelocal.net^/test-builds^/Club-VIP^/
echo ============================================================
echo.
pause
