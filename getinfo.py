import requests
import json
import asyncio

def update_modellist(models: list):
    with open("settings.json", 'r+') as file:
        data = json.load(file)
        data["models"] = models
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

def update_sampler(sampler: str):
    with open("settings.json", 'r+') as file:
        data = json.load(file)
        data["params"]["sampler"] = sampler
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

async def get_available_models() -> str:
    workers = requests.get(url="https://stablehorde.net/api/v2/workers").json()
    models = []
    for worker in workers:
        models = models + worker["models"]
    totmodels = list(dict.fromkeys(models))
    with open("acceptedmodels.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
    acceptedmodels = []
    for i in data:
        if(data[i]['modelname'] in totmodels):
            acceptedmodels.append(i)
    update_modellist(acceptedmodels)
    for i, mod in enumerate(acceptedmodels):
        acceptedmodels[i] = f"{'█' * models.count(data[mod]['modelname'])} {acceptedmodels[i]} {data[mod]['reactionname']}"
    return "Models available: \n" + '\n'.join(acceptedmodels)

async def get_status(api: str) -> str:
    with open("settings.json", 'r') as file:
        data = json.load(file)
    currentmodel = f"Default model: {data['defaultpayload']['models'][0]}"
    currentsampler = f"Default sampler: {data['defaultpayload']['params']['sampler_name']}"
    status_user = requests.get("https://stablehorde.net/api/v2/find_user", headers = {"apikey": api}).json()
    status = requests.get("https://stablehorde.net/api/v2/status/performance").json()
    bars = round(status_user["kudos"]/7000)
    bar = f"|{bars*'█'}{(20-bars)*'-'}|"
    return f"> {currentmodel}\n> {currentsampler}\n> {bar}\n> Generations available: ~{round(status_user['kudos']/10)}\n> Current Queue: {status['queued_requests']}\n> Current Workers: {status['worker_count']}"

