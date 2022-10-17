import random
import json

def is_float(str):
    try:
        float(str)
        return True
    except:
        return False

def is_int(str):
    try:
        int(str)
        return True
    except:
        return False

def parsecommand(inputstring):
    with open("settings.json", 'r') as file:
        settings = json.load(file)
    commanddict = {}
    
    #Seed
    if('-seed' in inputstring):
        if(is_int(inputstring[inputstring.index("-seed")+1])):
            commanddict["seed"] = inputstring.pop(inputstring.index("-seed")+1)
        else:
            commanddict["seed"] = str(random.randint(1, 10000))
        inputstring.pop(inputstring.index("-seed"))
    else:
        commanddict["seed"] = str(random.randint(1, 10000))
    
    #Step
    if('-s' in inputstring):
        if(is_int(inputstring[inputstring.index("-s")+1])):
            commanddict["step"] = int(inputstring.pop(inputstring.index("-s")+1))
        else:
            commanddict["step"] = settings["defaultpayload"]["steps"]
        inputstring.pop(inputstring.index("-s"))
    else:
        commanddict["step"] = settings["defaultpayload"]["steps"]
        
    #Guidance
    if('-g' in inputstring):
        if(is_float(inputstring[inputstring.index("-g")+1])):
            commanddict["guidance"] = float(inputstring.pop(inputstring.index("-g")+1))
        else:
            commanddict["guidance"] = settings["defaultpayload"]["cfg_scale"]
        inputstring.pop(inputstring.index("-g"))
    else:
        commanddict["guidance"] = settings["defaultpayload"]["cfg_scale"]
    
    #Prompt
    commanddict["prompt"] = " ".join(inputstring)

    return commanddict
