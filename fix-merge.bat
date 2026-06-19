@echo off
REM ============================================================
REM  fix-merge.bat  -  Escape the stuck merge and push SEO work
REM  Run this ONCE to unstick the current conflicted state.
REM  Your machine runs git as you, with your own credentials.
REM ============================================================
setlocal
cd /d "%~dp0"

echo.
echo [1/4] Aborting the broken merge (your committed SEO work is safe)...
git merge --abort 2>nul
git rebase --abort 2>nul

echo.
echo [2/4] Pulling remote changes, auto-taking remote's copy of any conflicts...
git pull --rebase -X theirs
if errorlevel 1 (
  echo.
  echo  !! Rebase hit something unexpected. Trying merge fallback...
  git pull --no-edit -X theirs
)

echo.
echo [3/4] Pushing your SEO commit to GitHub...
git push
if errorlevel 1 (
  echo.
  echo  !! Push failed. Scroll up to read the error, or send it to Claude.
  pause
  exit /b 1
)

echo.
echo [4/4] Done. GitHub has your changes; Vercel will auto-deploy in ~1-2 min.
echo.
echo  Note: your earlier 'git stash' (fitzgerald/vercel.json work) is still saved.
echo  To restore it later, run:  git stash pop
echo.
pause
