@echo off
REM One-time cleanup: remove accidental scratch files from git + disk, then deploy.
cd /d "%~dp0"
echo Removing scratch files from git tracking and disk...
git rm --cached -q _mountwrite_test.py _synctest.txt _synctest2.txt _vfinal.py 2>nul
del /q _mountwrite_test.py _synctest.txt _synctest2.txt _vfinal.py 2>nul
del /q _batchA.py _batchB.py _batchC.py _batchD.py _batchE.py _batchF.py 2>nul
echo Committing cleanup...
git add -A
git commit -m "chore: remove scratch/test files, gitignore them"
git pull --rebase -X theirs
git push
echo.
echo Done. Scratch files removed and deployed.
pause
