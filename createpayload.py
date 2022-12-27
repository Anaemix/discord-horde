import json
import asyncio
import re
import random
from math import ceil





def set_style(payload:dict, prompt:str):
    styles = json.load(open('styles.json','r'))
    style = prompt.split('style:')[1].strip()
    prompt = prompt.split('style:')[0].strip()
    if( "###" in prompt):
        p = prompt.split("###")[0]
        np = prompt.split("###")[1]
    else:
        p = prompt
        np = ""
    if(style in styles):
        for i in styles[style]:
            if i == "prompt":
                payload[i] = styles[style][i].replace("{p}", p).replace("{np}", "###"+np)
            elif i == "model":
                payload[i] = styles[style][i]
            else:
                payload['params'][i] = styles[style][i]
    return payload




def create_payload(prompt: str) -> dict:
    payload:dict = json.load(open("defaultpayload.json", "r"))
    if('style:' in prompt):
        payload = set_style(payload, prompt)
    else:
        payload['prompt'] = prompt
    return payload


def getheight(default:int, prompt:str):
    match = re.search("-h \d* ", prompt)
    if(match == None): return default, prompt
    else: prompt = re.sub("-h \d* ", "", prompt)
    h:int = int(match.group(0).split(" ")[1])
    h = min([ceil(h/64)*64, 1024])
    return h, prompt
    
def getwidth(default:int, prompt:str):
    match = re.search("-w \d* ", prompt)
    if(match == None): return default, prompt
    else: prompt = re.sub("-w \d* ", "", prompt)
    w:int = int(match.group(0).split(" ")[1])
    w = min([ceil(w/64)*64, 1024])
    return w, prompt

def getcfg(default:int, prompt:str):
    match = re.search("-cfg (\d|\.)* ", prompt)
    if(match == None): return default, prompt
    else: prompt = re.sub("-cfg (\d|\.)* ", "", prompt)
    c:float = float(match.group(0).split(" ")[1])
    c = ceil(c*2)/2
    return c, prompt

def getseed(prompt:str):
    match = re.search("-seed (\d)* ", prompt)
    if(match == None): return str(random.randint(0,10000)), prompt
    else: prompt = re.sub("-seed (\d)* ", "", prompt)
    s:int = int(match.group(0).split(" ")[1])
    return str(s), prompt

def getsampler(default:str, prompt:str):
    match = re.search("-sampler (\d)* ", prompt)
    if(match == None): return default, prompt
    else: prompt = re.sub("-sampler (\d)* ", "", prompt)
    s = match.group(0).split(" ")[1]
    return s, prompt

def getsteps(default:int, prompt:str):
    match = re.search("-steps (\d)* ", prompt)
    if(match == None): return default, prompt
    else: prompt = re.sub("-steps (\d)* ", "", prompt)
    s:int = int(match.group(0).split(" ")[1])
    s=min([max([s, 1]), 150])
    return s, prompt

def getmodel(default:str, prompt:str):
    with open("acceptedmodels.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
    for i in data:
        if(re.search(f"{i} ", prompt)):
            prompt = re.sub(f"{i} ", "", prompt)
            return [data[i]["modelname"]], prompt.strip() + data[i]["Keyword"]
    with open("settings.json", 'r') as file:
        settings = json.load(file)
    return default, prompt.strip()

def add_keyword(payload:dict):
    with open("acceptedmodels.json", "r", encoding='utf-8') as file:
        data = json.load(file)
    for i in data:
        if(payload["models"][0] == data[i]['modelname']):
            payload["prompt"] += data[i]['Keyword']
            return

"""def create_payload(prompt: str, id: str) -> dict:
    with open("users.json", "r", encoding="utf-8") as file:
        users = json.load(file)
    if id in users:
        default_model = [users[id]["model"]]
        default_sampler = users[id]["sampler_name"]
    else:
        default_model = payload["models"]
        default_sampler = payload["params"]["steps"]

    prompt = prompt + " "
    payload:dict = json.load(open("settings.json", "r"))["defaultpayload"]
    payload["params"]["height"], prompt = getheight(payload["params"]["height"], prompt)
    payload["params"]["width"], prompt = getwidth(payload["params"]["width"], prompt)
    payload["params"]["cfg_scale"], prompt = getcfg(payload["params"]["cfg_scale"], prompt)
    payload["params"]["seed"], prompt = getseed(prompt)
    payload["params"]["steps"], prompt = getsteps(payload["params"]["steps"], prompt)
    payload["params"]["sampler_name"], prompt = getsampler(default_sampler, prompt)
    if('style:' in prompt):
        payload = set_style(prompt)
    payload["models"], prompt = getmodel(default_model, prompt)
    payload["prompt"] = prompt
    add_keyword(payload)
    return payload

"""