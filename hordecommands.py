import asyncio
import json

async def setmodelglobal(arg: list) -> str:
    arg = (" ".join(arg)).strip()
    with open("acceptedmodels.json", "r+") as file:
        models = json.load(file)
    with open("settings.json", "r+") as file:
        data = json.load(file)
        if(arg in data['models'] and arg in list(models)):
            data['defaultpayload']['models'] = [models[arg]['modelname']]
            data['keyword'] = models[arg]['Keyword']
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
            return f"Global model changed to '{arg}'."
    return "Model not changed, model does not exist in model list. Try to run /models."

async def setsamplerglobal(arg: str) -> str:
    with open("settings.json", "r+") as file:
        data = json.load(file)
        if(arg in data['samplers']):
            data['defaultpayload']['params']['sampler_name'] = arg
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
            return f"Global sampler changed to '{arg}'."
    return f"Sampler not changed, available samplers are: {str(data['samplers'])}"

def get_website()->str:
    with open("settings.json", "r+") as file:
        data = json.load(file)
    return data["website"]

def info_model(arg: str) -> str:
    with open("acceptedmodels.json", 'r') as file:
        data = json.load(file)
    if(arg in list(data)):
        return f"> Modelname: {data[arg]['modelname']}\n> Description: {data[arg]['Description']}\n> Website: {data[arg]['Website']}\n> Keyword: '{data[arg]['Keyword']}'"
    return "No model with that tag."

