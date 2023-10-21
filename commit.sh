#!/bin/bash
python downloader.py >> log.txt
cp -R json /git/DL/ >> log.txt
cp index.json /git/DL/ >> log.txt
cd /git/DL/
timestamp=$(date +"at %H:%M:%S on %d.%m.%Y")
git add --all
git commit -am "Auto-commit $timestamp"
git push 



