import asyncio
import json

async def setmodelglobal(arg: list) -> str:
    arg = (" ".join(arg)).strip()
    with open("settings.json", "r+") as file:
        data = json.load(file)
        if(arg in data['models']):
            data['defaultpayload']['models'] = [arg]
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