@echo off
echo 推送更新到 GitHub...
git add .
git commit -m "Add brotli dependency for cloud deployment"
git push
echo 完成！
pause
