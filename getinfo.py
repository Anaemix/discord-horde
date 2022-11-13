import requests
import json
import asyncio

async def get_available_models():
    workers = requests.get(url="https://stablehorde.net/api/v2/workers").json()
    models = []
    for worker in workers:
        models = models + worker["models"]
    totmodels = list(dict.fromkeys(models))
    for i, mod in enumerate(totmodels):
        totmodels[i] = f"{'█' * models.count(mod)} {totmodels[i]}"
    return "\n".join(totmodels)

async def get_status(api):
    status_user = requests.get("https://stablehorde.net/api/v2/find_user", headers = {"apikey": api}).json()
    status = requests.get("https://stablehorde.net/api/v2/status/performance").json()
    bars = round(status_user["kudos"]/7000)
    bar = f"|{bars*'█'}{(20-bars)*'-'}|"
    return f"> {bar}\n> Generations available: ~{round(status_user['kudos']/10)}\n> Current Queue: {status['queued_requests']}\n> Current Workers: {status['worker_count']}"