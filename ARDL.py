# Auto-runer DL<T>

# _____/\\\\\\\\\_______/\\\\\\\\\______/\\\\\\\\\\\\_____/\\\_____________________________/\\\\\\\\\\\\\\\________________        
#  ___/\\\\\\\\\\\\\___/\\\///////\\\___\/\\\////////\\\__\/\\\_______________________/\\\_\///////\\\/////___/\\\__________       
#   __/\\\/////////\\\_\/\\\_____\/\\\___\/\\\______\//\\\_\/\\\____________________/\\\//________\/\\\_______\////\\\_______      
#    _\/\\\_______\/\\\_\/\\\\\\\\\\\/____\/\\\_______\/\\\_\/\\\_________________/\\\//___________\/\\\__________\////\\\____     
#     _\/\\\\\\\\\\\\\\\_\/\\\//////\\\____\/\\\_______\/\\\_\/\\\______________/\\\//______________\/\\\_____________\////\\\_    
#      _\/\\\/////////\\\_\/\\\____\//\\\___\/\\\_______\/\\\_\/\\\_____________\////\\\_____________\/\\\______________/\\\//__   
#       _\/\\\_______\/\\\_\/\\\_____\//\\\__\/\\\_______/\\\__\/\\\________________\////\\\__________\/\\\___________/\\\//_____  
#        _\/\\\_______\/\\\_\/\\\______\//\\\_\/\\\\\\\\\\\\/___\/\\\\\\\\\\\\\\\_______\////\\\_______\/\\\________/\\\//________ 
#         _\///________\///__\///________\///__\////////////_____\///////////////___________\///________\///________\///___________

import requests
from datetime import datetime
import os
def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

import time
import csv
import re
def windows_to_git_bash_path(windows_path):
    return re.sub(r'^([A-Z]):', lambda match: '/' + match.group(1).lower(), windows_path.replace('\\', '/'))
def win_api_eval(args):
    import subprocess
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    subprocess.call(args, startupinfo=si)


LINK_LIST_PATH = "./OTP_list.txt"
CSV_GOOGLE_SHEETS = "https://docs.google.com/spreadsheets/d/1HK9PHVXNUqVBaOeJLIoqog0mfiavo0IEN62jeeTr3Gs/export?format=csv&id=1HK9PHVXNUqVBaOeJLIoqog0mfiavo0IEN62jeeTr3Gs&gid=1422908853"
DEBUG = False
NEED_PRINT = True
CMD_RUN_SH = 'cd "'+os.path.dirname(__file__)+'" | commit.bat' # ["C:\Program Files (x86)\Git\git-bash.exe", "-c", "cd '"+windows_to_git_bash_path(os.path.dirname(__file__))+"';./commit.sh"]

if not NEED_PRINT:
    import sys
    sys.stdout = open(os.devnull, 'w')

session = requests.Session()

print('S', datetime.now().strftime("%d.%m.%Y %H:%M:%S.%f"), flush=True)
time.sleep(10);
while True:
    print('D', datetime.now().strftime("%d.%m.%Y %H:%M:%S.%f")+' ', end='',flush=True)
    decoded_content = session.get(CSV_GOOGLE_SHEETS, timeout=30).content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
    links = []
    with open(LINK_LIST_PATH, "r", encoding='utf-8') as f:
        for line in f:
            if re.match(r'^https:\/\/onlinetestpad\.com\/[a-zA-Z0-9]{13}$', line.strip()):
                links.append(line.strip())
    old_len = len(links)
    for row in my_list:
        for cell in row:
            if re.match(r'^https:\/\/onlinetestpad\.com\/[a-zA-Z0-9]{13}$', cell.strip()):
                links.append(cell.strip())
    links = f7(links)
    if old_len!=len(links):
        print('UPDATING...', end='',flush=True)
        with open(LINK_LIST_PATH, 'w', encoding='utf-8') as f:
            f.write('\n'.join(links));
        win_api_eval(CMD_RUN_SH)
    print('OK', flush=True)
    time.sleep(60*60*2);