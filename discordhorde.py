import discord
from discord.ext import commands
import asyncio
import requests
import base64
import time
import os
import json

import createpayload
import hordecommands
import getinfo

url = "https://stablehorde.net/api/"

bot = commands.Bot(command_prefix='/')

with open("settings.json", 'r') as file:
    settings = json.load(file)






class discord_horde_request:
    ETA = "N/A"
    Queue = 0
    def __init__(self, context, promptlist):
        self.context = context
        self.promptlist = promptlist
        self.payload = createpayload.create_payload(" ".join(promptlist))
        self.index = str(time.time()).replace(".","")

    #Requests generation process
    async def generate(self):
        self.api_key = settings["apikey"]
        try:
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

@bot.command()
async def setsamplerglobal(ctx, arg):
    message = await hordecommands.setsamplerglobal(arg.strip())
    await ctx.send(message)

@bot.command()
async def setmodelglobal(ctx, *arg):
    message = await hordecommands.setmodelglobal(list(arg))
    await ctx.send(message)

@bot.command()
async def models(ctx):
    modelsmessage = await getinfo.get_available_models()
    await ctx.send(modelsmessage)

@bot.command()
async def status(ctx):
    statusmessage = await getinfo.get_status(settings["apikey"])
    await ctx.send(statusmessage)

@bot.command()
async def create(ctx, *arg):
    obj = discord_horde_request(ctx, list(arg))
    task = asyncio.create_task(obj.generate())
    await task
    
@bot.command()
async def reboot(ctx):
    await ctx.send("Restarting bot... ")
    os.system("sudo shutdown -r now")

if __name__ == "__main__":
    bot.run(settings["discord"])