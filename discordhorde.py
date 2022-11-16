import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import requests
import base64
import time
import os
import json

import createpayload
import hordecommands
import getinfo
from helpmessages import *

url = "https://stablehorde.net/api/"

bot = commands.Bot(command_prefix='/')

with open("settings.json", 'r') as file:
    settings = json.load(file)




global model_message

class discord_horde_request:
    ETA = "N/A"
    Queue = 0
    def __init__(self, context, promptlist):
        self.context = context
        self.promptlist = promptlist
        self.payload = createpayload.create_payload(" ".join(promptlist), str(context.message.author.id))
        self.index = str(time.time()).replace(".","")
        try:
            with open("users.json", 'r', encoding='utf-8') as file:
                users = json.load(file)
            if(users[str(context.message.author.id)]['log_prompts']):
                self.log_prompt(self)
        except:
            pass

    #Requests generation process
    async def generate(self):
        self.api_key = settings["apikey"]
        try:
            print(self.payload)
            response = requests.post(url=url+"v2/generate/async", json= self.payload, headers = {"apikey": self.api_key}).json()
            self.id = response['id']
            await self.message_created()
            await self.poll()
        except:
            print("failed to generate:", response)
            return 1

    #Sends generating message
    async def message_created(self):
        self.message = await self.context.send("Generating Image...")
        self.time_started = time.time()
        self.time_elapsed = 0

    #Updates message
    async def update_message(self):
        if(self.Queue>0):
            await self.message.edit(content=f"Generating Image... <In queueposition: {self.Queue}>")
        else:
            await self.message.edit(content=f"Generating Image... <ETA: {self.ETA+1}>")

    async def delete_update_message(self):
        await self.message.delete()

    #Polls if Image is done each second
    async def poll(self):
        await asyncio.sleep(1)
        self.time_elapsed=time.time()-self.time_started
        response = requests.get(url=url+f"v2/generate/check/{self.id}").json()
        self.ETA = response["wait_time"]
        self.Queue = response["queue_position"]

        if (self.time_started+self.time_elapsed)>self.time_started+2:
            await self.update_message()
        if(response['finished'] == 1):
            await self.get_finished_image()
        else:
            await self.poll()
    
    #Downloads image if it's done
    async def get_finished_image(self):
    
        self.filepath = self.index + ".webp"
        returned_img=requests.get(url=url+f"v2/generate/status/{self.id}").json()['generations'][0]['img']
        data = bytes(returned_img, "utf-8")
        with open(self.filepath,'wb') as file:
            file.write(base64.b64decode(data))
        await self.return_image()
        await self.delete_update_message()
    
    #Sends back image over discord if it's done
    async def return_image(self):
        await asyncio.sleep(0.1)
        self.time_elapsed = time.time()-self.time_started
        file = discord.File(self.filepath, filename = self.filepath)
        await self.context.send(f"{self.context.author.name}'s image done in {round(self.time_elapsed)}s! with seed {self.payload['params']['seed']}" , file = file)
        os.remove(self.filepath)

    def log_prompt(self):
        with open(f"logs/{str(self.context.message.author.id)}.txt", 'a', encoding='utf-8') as file:
            file.write(f"{self.payload}\n")

@bot.event
async def on_ready():
    channel = bot.get_channel(1015193537228312576)
    message = await getinfo.get_available_models()
    try:
        msg = await channel.fetch_message(settings['model_message'])
        await msg.delete()
    except:
        pass
    msg = await channel.send(message)
    with open("settings.json", 'r+') as file:
        data = json.load(file)
        data["model_message"] = msg.id
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
    with open("acceptedmodels.json", 'r+', encoding='utf-8') as file:
        models = json.load(file)
    for model in models:
        #print(models[model]["reaction"])
        await msg.add_reaction(models[model]["reaction"])
    global model_message
    model_message = msg
    

@bot.event
async def on_reaction_add(reaction, user):
    if not user.bot and reaction.message == model_message:
        with open("acceptedmodels.json", 'r+', encoding='utf-8') as file:
            models = json.load(file)
        
        for i in models:
            if(reaction.emoji == models[i]["reaction"]):
                hordecommands.set_user(str(user.id), user.name, model=models[i]["modelname"])
                await reaction.message.channel.send(f"{user.name}'s model is set to {models[i]['modelname']}")
                break
        
"""
@bot.command()
async def test(ctx, arg):
    await ctx.send(str(ctx.message.author.id))
"""
@bot.command()
async def info(ctx, arg, description=help_info):
    message = hordecommands.info_model(arg)
    await ctx.send(message)

@bot.command()
async def github(ctx, description=help_github):
    message = hordecommands.get_website()
    await ctx.send(message)

@bot.command()
async def setsamplerglobal(ctx, arg, description=help_setsamplerglobal):
    message = await hordecommands.setsamplerglobal(arg.strip())
    await ctx.send(message)

@bot.command()
async def setmodelglobal(ctx, *arg, description=help_setmodelglobal):
    message = await hordecommands.setmodelglobal(list(arg))
    await ctx.send(message)

@bot.command()
async def models(ctx, description=help_models):
    modelsmessage = await getinfo.get_available_models()
    await ctx.send(modelsmessage)

@bot.command()
async def status(ctx, description=help_status):
    statusmessage = await getinfo.get_status(settings["apikey"])
    last_status = await ctx.send(statusmessage)

@bot.command()
async def create(ctx, *arg, description=help_create):
    obj = discord_horde_request(ctx, list(arg))
    task = asyncio.create_task(obj.generate())
    await task
    
@bot.command()
async def reboot(ctx):
    await ctx.send("currently disabled")
    #await ctx.send("Restarting bot... ")
    #os.system("sudo shutdown -r now")

if __name__ == "__main__":
    bot.run(settings["discord"])