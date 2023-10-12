python downloader.py >> log.txt
xcopy "json" "D:/git/DL/json" /Y >> log.txt
copy index.json D:/git/DL/index.json >> log.txt
cd D:/git/DL/
git add --all
NOW=$(date +"%m-%d-%Y %H:%M:%S")
git commit -am "Auto-commit at: $NOW"
git push