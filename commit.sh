python downloader.py >> log.txt
cp -R json /git/DL/ >> log.txt
cp index.json /git/DL/ >> log.txt
cd /git/DL/
git add --all
timestamp() {
  date +"at %H:%M:%S on %d.%m.%Y"
}
git commit -am "Auto-commit $(timestamp)"
git push