python downloader.py >> log.txt
xcopy "json" "D:/git/DL/json" /Y >> log.txt
copy index.json D:/git/DL/index.json >> log.txt
cd D:/git/DL/
git add --all
git commit -am "Auto-commit at: %DATE% %TIME%"
git push