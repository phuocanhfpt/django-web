@echo off
set REPO_NAME=django_demo
set BFG_JAR=D:\Tools\bfg.jar
set REPO_DIR=D:\Projects\%REPO_NAME%
set MIRROR_DIR=%REPO_DIR%.git
set REPLACE_FILE=%REPO_DIR%\replacements.txt

echo === Đang clone dạng mirror ===
git clone --mirror %REPO_DIR% %MIRROR_DIR%

echo === Đang chạy BFG để xoá secrets ===
java -jar %BFG_JAR% --replace-text %REPLACE_FILE% %MIRROR_DIR%

echo === Làm sạch dữ liệu cũ ===
cd %MIRROR_DIR%
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo === Push lên GitHub (force) ===
git push --force

echo === XONG ===
pause