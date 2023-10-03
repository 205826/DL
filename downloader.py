
# __/\\\\\\\\\\\\_____/\\\_____________________________/\\\\\\\\\\\\\\\________________        
#  _\/\\\////////\\\__\/\\\_______________________/\\\_\///////\\\/////___/\\\__________       
#   _\/\\\______\//\\\_\/\\\____________________/\\\//________\/\\\_______\////\\\_______      
#    _\/\\\_______\/\\\_\/\\\_________________/\\\//___________\/\\\__________\////\\\____     
#     _\/\\\_______\/\\\_\/\\\______________/\\\//______________\/\\\_____________\////\\\_    
#      _\/\\\_______\/\\\_\/\\\_____________\////\\\_____________\/\\\______________/\\\//__   
#       _\/\\\_______/\\\__\/\\\________________\////\\\__________\/\\\___________/\\\//_____  
#        _\/\\\\\\\\\\\\/___\/\\\\\\\\\\\\\\\_______\////\\\_______\/\\\________/\\\//________ 
#         _\////////////_____\///////////////___________\///________\///________\///___________

from FileDB import FileDB
import requests
import xml.etree.ElementTree as ET
from html.parser import HTMLParser


DB_PATH = "./__cache/"
LINK_LIST_PATH = "./OTP_list.txt"
EXPORT_JSON_NAME = "./index.json"
EXPORT_JSON_NAME_GENERATOR = lambda i,name: ("./json/output_"+str(i)+".json", "json/output_"+str(i)+".json"); # (1..n, "Рубежный теортест ...") => save_to, js_path
SAVING_EVERY_N = 10
DEBUG = False
NEED_PRINT = True
ERROR_CORRECTION = True

if not NEED_PRINT:
    import sys, os
    sys.stdout = open(os.devnull, 'w')

mydb = FileDB(DB_PATH)
session = requests.Session()

is_with_answers = {}
links = [v for v in [line.strip() for line in open(LINK_LIST_PATH, "r")] if v]

need_save=False
for i in range(0, len(links)):
    print(str(i+1)+'. loading '+links[i]+'... ', end='')
    cache = mydb.get(links[i])
    if cache:
        print('cached!')
        links[i]=cache
    else:
        need_save=True
        x=False;
        while not x:
            try:
                x = session.get(links[i], timeout=30).text
            except:
                print('E!', end='')
        print('OK!')
        mydb.set(links[i] , x)
        print('seted!')
        links[i]=x

print("Parsing...")


for i in range(0,len(links)):
    print(str(i+1)+". ", end='')
    html_stack = []
    title = ""
    results = []
    tasks = []
    error_title = ""
    
    class MyHTMLParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            global error_title;
            s=tag
            for attr in attrs:
                if attr[0] == "id":
                    s+="#"+attr[1]
                elif (attr[0] == "class")and(attr[1].strip()):
                    s+="."+attr[1].strip().replace(" ",".")
            html_stack.append(s)
            if "div#dQuestions" in html_stack:
                # init
                if html_stack[-2] == "div#dQuestions":
                    tasks.append({"question": "", "question_img": "", "answers": [], "errors": []})
                    print(str(len(tasks))+' ', end='')
                
                # question
                if ("div.image" in html_stack)and(s=="img"):
                    tasks[-1]["question_img"]+=dict(attrs)["src"]
                if ("span.qtext" in html_stack)and(s=="img")and("data-formula" in dict(attrs)):
                    import urllib.parse
                    tasks[-1]["question"]+='$$'+urllib.parse.unquote(dict(attrs)["data-formula"])+'$$'
                
                # answers
                if "div#d-q-ans-container" in html_stack:
                    if (s == "div.item.otp-row-2")or(s == "div.item.otp-row-1")or(s == 'tr'):
                        tasks[-1]["answers"].append({"type": "", "value": "", "text":"", "image":""})
                    if s=="img.ans-img":
                        tasks[-1]["answers"][-1]["image"]+=dict(attrs)["src"]
                    if ("span" in html_stack) and (s == "img")and("data-formula" in dict(attrs)):
                        import urllib.parse
                        tasks[-1]["answers"][-1]["text"]+='$$'+urllib.parse.unquote(dict(attrs)["data-formula"])+'$$'
                    if s[:5]=="input":
                        input_type = dict(attrs)["type"]
                        tasks[-1]["answers"][-1]["type"]=input_type
                        if (input_type=="radio")or(input_type=="checkbox"):
                            tasks[-1]["answers"][-1]["value"]="CHECKED" if "checked" in dict(attrs) else "UNCHECKED"
                        elif input_type=="text":
                            tasks[-1]["answers"][-1]["value"]=dict(attrs)["value"]
                
                # errors
                if "div.rightanswers" in html_stack:
                    if ("div.item"==s)or(("table.item" in html_stack) and ("tr"==s)):
                        tasks[-1]["errors"].append({"type": error_title, "text": "", "image": ""});
                    if ("div.item" in html_stack)and("img.ans-img" in html_stack):
                        tasks[-1]["errors"][-1]["image"]+=dict(attrs)["src"]
                    if ("div.item" in html_stack)and("span" in html_stack)and (s == "img")and("data-formula" in dict(attrs)):
                        import urllib.parse
                        tasks[-1]["errors"][-1]["text"]+='$$'+urllib.parse.unquote(dict(attrs)["data-formula"])+'$$'
                    
                    

        def handle_data(self, data):
            # title
            global title;
            global error_title;
            if ("h1.otp-item-view-title" in html_stack)and("span" in html_stack):
                title+=data
            
            if "div#dQuestions" in html_stack:
                # question text
                if "span.qtext" in html_stack:
                    tasks[-1]["question"]+=data
                
                # answer text
                if "div#d-q-ans-container" in html_stack:
                    if "span" in html_stack:
                        tasks[-1]["answers"][-1]["text"]+=data.strip()
                # errors
                if "div.rightanswers" in html_stack:
                    if ("span.blocktitle" in html_stack) and (data.strip()):
                        error_title=data.strip()
                    if ("div.item" in html_stack)and("span" in html_stack):
                        tasks[-1]["errors"][-1]["text"]+=data.strip()
                    if ("table.item" in html_stack)and("b.row" in html_stack)and(data):
                        tasks[-1]["errors"][-1]["type"]+="replace on "+data.strip()
                    if ("table.item" in html_stack)and("span.correctans.otp-item-ans-correct" in html_stack)and(data):
                        tasks[-1]["errors"][-1]["type"]+=" to "+data.strip()
                        
            
            # result
            if ("table.table.item-table-results" in html_stack)and("td" in html_stack):
                results.append(data.strip())
        
        def handle_endtag(self, tag):
            html_stack.pop()
                    
                

    import re
    MyHTMLParser().feed(re.sub('<(link|meta) .*" *?>', '', links[i]))

    results = [float(results[1]), int(results[3])]
    title=title.strip()

    print(title+': '+str(results[0])+'/'+str(results[1]))
    if DEBUG:
        print(tasks)
    links[i] = {"title": title, "tasks": tasks, "correct_answers": results[0], "total_answers": results[1]}
    is_with_answers[title] = False



print("Downloading iamges...")
image_dict = {}
def get_base64_image(url):
    import base64
    import requests
    cache = mydb.get(url)
    if cache:
        return cache
    else:
        print('L:', end='')
        b = base64.b64encode(session.get(url).content).decode('utf-8')
        print('OK!S:', end='')
        mydb.set(url, b)
        print('OK! ', end='')
        return b

i=1
for solution in links: 
    print(str(i)+'. ', end='')
    i+=1
    if solution["title"] not in image_dict:
        image_dict[solution["title"]] = {}
    def add_img(url):
        if url not in image_dict[solution["title"]]:
            image_dict[solution["title"]][url]=get_base64_image(url)
    for task in solution["tasks"]:
        if task["question_img"]:
            add_img(task["question_img"])
        for answer in task["answers"]:
            if answer["image"]:
                add_img(answer["image"])
    print('DONE!')

if True:
    print("Error correction...")

    i=1
    for solution in links:
        print(str(i)+'. ', end='')
        i+=1
        j=1
        for task in solution["tasks"]:
            print(str(j)+' ', end='')
            j+=1
            
            ttype = ""
            if task["answers"][0]["type"] == "checkbox":
                ttype = "multiselect"
            elif task["answers"][0]["type"] == "text":
                ttype = "strings"
            elif task["answers"][0]["type"] == "radio":
                ttype = "singleselect"
            
            if not ttype:
                print('Type error! ', end='')
            for answer in task["answers"]:
                if answer["type"] != task["answers"][0]["type"]:
                    print('Parse error! ', end='')
            task["type"] = ttype
            if ERROR_CORRECTION:
                for error in task["errors"]:
                    is_with_answers[solution["title"]] = True;
                    if ttype == "multiselect":
                        if error["type"] == "Не выбрано:":
                            t = 0
                            for answer in task["answers"]:
                                if (answer["text"]==error["text"])and(answer["image"]==error["image"]):
                                    answer["value"]="CHECKED"
                                    t+=1
                            if t!=1:
                                print('Parse error2! ', end='')
                        elif error["type"] == "Выбрано лишнее:":
                            t = 0
                            for answer in task["answers"]:
                                if (answer["text"]==error["text"])and(answer["image"]==error["image"]):
                                    answer["value"]="UNCHECKED"
                                    t+=1
                            if t!=1:
                                print('Parse error3! ', end='')
                        else:
                            print('Undefined type2! ', end='')
                    elif ttype == "singleselect":
                        if error["type"] == "Правильный ответ:":
                            t = 0
                            for answer in task["answers"]:
                                if (answer["text"]==error["text"])and(answer["image"]==error["image"]):
                                    answer["value"]="CHECKED"
                                    t+=1
                                else:
                                    answer["value"]="UNCHECKED"
                            if t!=1:
                                print('Parse error4! ', end='')
                        else:
                            print('Undefined type3! ', end='')
                    elif ttype == "strings":
                        import re
                        t = re.findall(r'replace on (.*) to (.*)', error["type"])
                        if len(t)==1:
                            task["answers"][int(t[0][0])-1]["value"] = t[0][1]
                        else:
                            print('Type error2! ')
                    else:
                        print('Undefined type! ', end='')
            task.pop("errors", 0)
        print('DONE!')
    for solution in links:
        if is_with_answers[solution["title"]]:
            solution["correct_answers"] = float(solution["total_answers"])

#print("Export json (For what?)...")
#import json
#with open("output.json", 'w') as f:
#    f.write(json.dumps(links, ensure_ascii=False))

print("Solution to test")
all_tests = {}
# {
#   [
#      {
#         type: ""
#         number: 0
#         text: ""
#         image: ""
#         answers: [{text:"", image:"", solutions: [{id: 0, value:"", result: 0.0, result_max: 12}, ...]}]
#       }
#   ]
# }


i=1
for solution in links:
    print(str(i)+'. ', end='')
    i+=1
    if solution["title"] not in all_tests:
        all_tests[solution["title"]] = []
    j=1
    for task in solution["tasks"]:
        out_task = {}
        out_task["type"] = task["type"]
        out_task["number"] = j
        out_task["text"] = task["question"]
        out_task["image"] = task["question_img"]
        out_task["answers"] = []
        for answer in task["answers"]:
            out_task["answers"].append({"text": answer["text"], "image": answer["image"], "solutions": [{"id": i, "value": answer["value"], "result": solution["correct_answers"], "result_max": solution["total_answers"]}]})

        
        def merge_answer(to, add):
            mflag = True
            for e in to:
                if (e["text"] == add["text"]) and (e["image"] == add["image"]):
                    for k in add["solutions"]:
                        e["solutions"].append(k)
                    mflag = False
            if mflag:
                to.append(add);
        
        def merge_task(to, add):
            mflag = True
            for e in to:
                if (e["type"] == add["type"]) and (e["number"] == add["number"]) and (e["text"] == add["text"]) and (e["image"] == add["image"]):
                    if out_task["type"]=="strings":
                        for i,k in enumerate(add["answers"]):
                            e["answers"][i]["solutions"].append(k["solutions"][0])
                    else:
                        for k in add["answers"]:
                            merge_answer(e["answers"],k)
                    mflag = False
            if mflag:
                to.append(add);
        
        merge_task(all_tests[solution["title"]],out_task)
        
        j+=1
        

    print("DONE!")




print("Saving... ")

index_json = {}
#{
#  name: {
#    json: "js_path"
#    with_answers: T/F
#  }
#}
i=0
for name in sorted(all_tests.keys()):
    if name[0] != '_':
        i+=1
        index_json[name] = {"title": name, "json": EXPORT_JSON_NAME_GENERATOR(i, name)[1], "with_answers": is_with_answers[name]}
print("0. "+EXPORT_JSON_NAME)
import json
with open(EXPORT_JSON_NAME, 'w', encoding='utf-8') as f:
    f.write(json.dumps(index_json, ensure_ascii=False))

i=0
for name in sorted(all_tests.keys()):
    i+=1
    print(str(i)+". "+EXPORT_JSON_NAME_GENERATOR(i, name)[0])
    
    with open(EXPORT_JSON_NAME_GENERATOR(i, name)[0], 'w', encoding='utf-8') as f:
        f.write(json.dumps({"images": image_dict[name], "tasks": all_tests[name]}, ensure_ascii=False))

print("END!")

# print("TODO: Task resolving...")
# import subprocess
# subprocess.call(["resolver.exe"]) #TODO

# Idea for resolver
# tests = [[100%, 4,2,7,..1], [90%, 1,2,7,..1]].map(x=>x[0]=x[0]*(x.length-1))
# sort tests by x[0] 
# tasks = [
#     //[yes_probability,yes_probability,...]
#     [0.5, 0.5, 0.5,...]
#     [0.5, 0.5, 0.5,...]
#     ...
#     [0.5, 0.5, 0.5,...]
# ]
# for test in tests:
#     for task in test:
#         tasks[task].yes_probability=test.probability if selected yes else 1-test.probability
#         for test2 in tests where task in test2:
#             test2.probability-=test.probability
#             test2.pop(tasks)




   
