python downloader.py >> log.txt
cp -R json /d/git/DL/
cp index.json /d/git/DL/
cd /d/git/DL/
git add --all
timestamp() {
  date +"at %H:%M:%S on %d.%m.%Y"
}
git commit -am "Auto-commit $(timestamp)"
git push