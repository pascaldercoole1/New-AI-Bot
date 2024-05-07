import discord
from discord.ext import commands
import os
from leptonai.client import Client
from keep_alive import keep_alive
import random
import time
import datetime
import openai
import requests

image_count = 0
voice_count = 0
text_count = 0
start_time = time.time()

api_token = os.environ.get('api')
lepton_client = Client("https://sdxl.lepton.run", token=api_token)

intents = discord.Intents.default()
intents.messages = True 
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    keep_alive()
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def generate(ctx, *, prompt):
    global image_count
    try:
        GeneratingImageMessage = await ctx.send(f"Generating Image... :hourglass_flowing_sand:")
        untere_grenze = 1
        obere_grenze = 5000000000
        zufallszahl = random.randint(untere_grenze, obere_grenze)
        
        image = lepton_client.run(
            prompt=prompt,
            height=1024,
            width=1024,
            guidance_scale=5,
            high_noise_frac=0.75,
            seed=zufallszahl,
            steps=30,
            use_refiner=False
        )
        with open(f'output_image_{str(zufallszahl)}.png', 'wb') as f:
            f.write(image)

        await GeneratingImageMessage.delete()
        await ctx.send(f"Image Generating Done! :white_check_mark:")
        await ctx.send(file=discord.File(f'output_image_{str(zufallszahl)}.png'))
        os.remove(f'output_image_{str(zufallszahl)}.png')  
        
        image_count += 1
    except Exception as e:
        print(f"An error occurred: {e}")

@bot.command()
async def p(ctx, *, prompt):
    global image_count
    try:
        GeneratingImageMessage = await ctx.send(f"Generating Image... :hourglass_flowing_sand:")
        untere_grenze = 1
        obere_grenze = 5000000000
        zufallszahl = random.randint(untere_grenze, obere_grenze)

        url = "https://pornworks.ai/api/v2/generate/text2image"

        def Check(f):
            url = f"https://pornworks.ai/api/v2/generations/{f}/state"

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "no-cors",
                "Sec-Fetch-Site": "same-origin",
                "Site": "pornworks",
                "Currency": "EUR",
                "cf-auth-token": "eyJ4IjoiL2dlbmVyYXRlO2dlbmVyYXRpb249YTlhYTQyYzQtMWVjNi00NzVlLWFlYmQtNWJkOTk1OGFmZTc2IiwibGciOiJkZSIsImplIjpmYWxzZSwiZGgiOjEwODAsImR3IjoxOTIwLCJjZCI6MjQsInRvIjoiLTEyMCIsInUiOiIzRVE5aWZ2cFYiLCJ6IjoiaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8ifQ=="
            }

            response = requests.get(url, headers=headers)
            print("response:",response.text)
            state = response.json()["state"]
            if state == "pending":
                return {"state":state, "Image":"/"}
            else:
                ImageURL = response.json()["results"]["image"]
                return {"state":state, "Image":"https://pornworks.ai"+str(ImageURL)}
            
        cookies = {
            "user-token": "c4374ccd-6359-419a-a1d3-c59208fce047"
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
            "Content-Type": "application/json",
            "Site": "pornworks",
            "Currency": "EUR",
            "cf-auth-token": "eyJ4IjoiL2dlbmVyYXRlO2dlbmVyYXRpb249YTlhYTQyYzQtMWVjNi00NzVlLWFlYmQtNWJkOTk1OGFmZTc2IiwibGciOiJkZSIsImplIjpmYWxzZSwiZGgiOjEwODAsImR3IjoxOTIwLCJjZCI6MjQsInRvIjoiLTEyMCIsInUiOiIzRVE5aWZ2cFYiLCJ6IjoiaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8ifQ==",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
        }

        data = {
            "baseModel": "SD 1.5",
            "checkpoint": "realistic_v3",
            "prompt": prompt,
            "negativePrompt": "High pass filter, airbrush,portrait,zoomed, soft light, smooth skin,closeup, Anime, fake, cartoon, deformed, extra limbs, extra fingers, mutated hands, bad anatomy, bad proportions , blind, bad eyes, ugly eyes, dead eyes, blur, vignette, out of shot, out of focus, gaussian, closeup, monochrome, grainy, noisy, text, writing, watermark, logo, oversaturation , over saturation, over shadow, floating limbs, disconnected limbs, anime, kitsch, cartoon, penis, fake, (black and white), airbrush, drawing, illustration, boring, 3d render, long neck, out of frame, extra fingers, mutated hands, monochrome, ((poorly drawn hands)), ((poorly drawn face)), (((mutation))), (((deformed))), ((ugly)), blurry, ((bad anatomy)), (((bad proportions))), ((extra limbs)), cloned face, glitchy, bokeh, (((long neck))), (child), (childlike), 3D, 3DCG, cgstation, red eyes, multiple subjects, extra heads, close up, man, ((asian)), text, bad anatomy, morphing, messy broken legs decay, ((simple background)), deformed body, lowres, bad anatomy, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low jpeg artifacts, signature, watermark, username, blurry, out of focus, old, amateur drawing, odd, fat, morphing, ((simple background)), artifacts, signature, artist name, [blurry], disfigured, mutated, (poorly hands), messy broken legs, decay, painting, duplicate, closeup",
            "resources": [],
            "samplerName": "DPM++ 2M Karras",
            "size": "512x768",
            "hr": False,
            "cfgScale": 5,
            "performance": "speed",
            "denoisingStrength": 1,
            "fast": False,
            "nsfw": True,
            "inpaintMode": "checkpoint"
        }


        response = requests.post(url, json=data, headers=headers, cookies=cookies)
        print("response:",response,response.text)
        print(response.json())
        id = response.json()["id"]
        print("ID:",id)
        Check(id)

        timealr = 0

        while True:
            try:
                status = Check(id)
                if status["state"] == "done":
                    print(status["Image"])
                    #with open(f'output_image_{str(zufallszahl)}.png', 'wb') as f:
                    #    f.write(image)
                    await GeneratingImageMessage.delete()
                    await ctx.send(f"Image Generating Done! :white_check_mark:")
                    response = requests.get(status["Image"])
                    if response.status_code == 200:
                        with open("pornimage.png", "wb") as f:
                            f.write(response.content)
                    else:
                        print("Failed to download the image. Status code:", response.status_code)

                    await ctx.send(file=discord.File(f'pornimage.png'))
                    os.remove(f'pornimage.png')  

                    #await ctx.send(file=discord.File(f'output_image_{str(zufallszahl)}.png'))
                    #os.remove(f'output_image_{str(zufallszahl)}.png')  
                    
                    image_count += 1
                    break
                time.sleep(1)
                timealr = timealr + 1
                await GeneratingImageMessage.edit(content="Generating Image... :hourglass_flowing_sand: | "+str(timealr))
            except:
                print("Weird getting Status")
                time.sleep(3)

        
    except Exception as e:
        print(f"An error occurred: {e}")



@bot.command()
async def generate2(ctx, *, prompt):
    global image_count
    try:
        GeneratingImageMessage = await ctx.send(f"Generating Image... :hourglass_flowing_sand:")
        untere_grenze = 1
        obere_grenze = 5000000000
        zufallszahl = random.randint(untere_grenze, obere_grenze)

        c2 = Client("https://sdxl.lepton.run", token=api_token)

        image = c2.run(
            prompt=prompt,
            height=1024,
            width=1024,
            guidance_scale=5,
            high_noise_frac=0.75,
            seed=zufallszahl,
            steps=30,
            use_refiner=False
        )
        with open(f'output_image_{str(zufallszahl)}.png', 'wb') as f:
            f.write(image)

        await GeneratingImageMessage.delete()
        await ctx.send(f"Image Generating Done! :white_check_mark:")
        await ctx.send(file=discord.File(f'output_image_{str(zufallszahl)}.png'))
        os.remove(f'output_image_{str(zufallszahl)}.png')  
        
        image_count += 1
    except Exception as e:
        print(f"An error occurred: {e}")

@bot.command()
async def text(ctx, *, prompt):
    global text_count
    try:
        GeneratingImageMessage = await ctx.send(f"Generating Text... :hourglass_flowing_sand:")
        untere_grenze = 1
        obere_grenze = 5000000000
        zufallszahl = random.randint(untere_grenze, obere_grenze)

        client = openai.OpenAI(
            base_url="https://gemma-7b.lepton.run/api/v1/",
            api_key=api_token
        )

        completion = client.chat.completions.create(
            model="gemma-7b",
            messages=[
                {"role": "user", "content": prompt},
            ],
            max_tokens=100000,
            stream=True,
        )

        currentex = ""

        for chunk in completion:
            if not chunk.choices:
                continue
            content = chunk.choices[0].delta.content
            if content:
                # print(content, end="")
                currentex = currentex + str(content)

        await GeneratingImageMessage.delete()
        GeneratingImageMessage2 = await ctx.send(f"Text Generation Done! :white_check_mark:")
        await ctx.send(currentex)
        time.sleep(1)
        await GeneratingImageMessage2.delete()
        
        text_count += 1
    except Exception as e:
        print(f"An error occurred: {e}")


def convert_to_format(data):
    result = ""
    for i, segment in enumerate(data):
        text = segment['text']
        start_time = segment['start']
        end_time = segment['end']
        formatted_text = f"[{start_time:.2f}-{end_time:.2f}]\n```{text}```\n"
        result += formatted_text
    return result

def convert_to_formatfile(data):
    result = ""
    for i, segment in enumerate(data):
        text = segment['text']
        start_time = segment['start']
        end_time = segment['end']
        formatted_text = f"[{start_time:.2f}-{end_time:.2f}]\n{text}\n"
        result += formatted_text
    return result

@bot.command()
async def ToText(ctx):
    try:
        if ctx.message.attachments:  
            attachment = ctx.message.attachments[0]  
            file_url = attachment.url 
            #if file_url.endswith('.mp3'):
            ToTextCLIENT = Client("https://whisperx.lepton.run", token=api_token)
            GeneratingTextMessage = await ctx.send(f"Generating Text... :hourglass_flowing_sand:")
            result=ToTextCLIENT.run(
                input=file_url
            )
            #print("result:",result, convert_to_format(result))
            Final = convert_to_format(result) # result[0]["text"]
            print("FI:",Final)
            if len(Final) > 2000:
                print("MEHR ALS 2k")
                untere_grenze = 1
                obere_grenze = 5000000000
                zufallszahl = random.randint(untere_grenze, obere_grenze)

                Final = convert_to_formatfile(result)

                print("YO",zufallszahl)
                with open(f'output_text_{str(zufallszahl)}.txt', 'wb') as f:
                    f.write(Final.encode())

                
                await GeneratingTextMessage.delete()
                await ctx.send(f"Text Generating Done! :white_check_mark:")
                await ctx.send(file=discord.File(f'output_text_{str(zufallszahl)}.txt'))

                os.remove(f'output_text_{str(zufallszahl)}.txt')  
            else:
                print("OK",Final)
                await GeneratingTextMessage.delete()
                await ctx.send(f"Text Generating Done! :white_check_mark:")
                await ctx.send(f"Your Responce:```{Final}")
            #else:
            #    await ctx.send("Please upload a MP3 File.")
        else:
            await ctx.send("I dont see your File...?")
    except Exception as e:
        print("ERROR", e)




@bot.command()
async def voice(ctx, *, prompt):
    global voice_count
    try:
        c = Client("https://openvoice.lepton.run", token=api_token)
        
        untere_grenze = 1
        obere_grenze = 5000000000
        zufallszahl = random.randint(untere_grenze, obere_grenze)

        GeneratingVoiceMessage = await ctx.send(f"Generating Voice... :hourglass_flowing_sand:")

        mpeg=c.run(
            reference_speaker="https://www.lepton.ai/playground/openvoice/inputs/speaker_1.mp3",
            text=prompt,
            emotion="friendly"
        )
        with open(f'output_image_{zufallszahl}.mp3', 'wb') as f:
            f.write(mpeg)

        await GeneratingVoiceMessage.delete()
        await ctx.send(f"Voice Generating Done! :white_check_mark:")
        await ctx.send(file=discord.File(f'output_image_{zufallszahl}.mp3'))
        os.remove(f'output_image_{zufallszahl}.mp3')
        
        voice_count += 1
    except Exception as e:
        print(f"An error occurred: {e}")

@bot.command()
async def uptime(ctx):
    global start_time
    current_time = time.time()
    uptime_seconds = int(current_time - start_time)
    uptime_string = str(datetime.timedelta(seconds=uptime_seconds))
    await ctx.send(f"Uptime: {uptime_string}")

@bot.command()
async def invite(ctx):
    await ctx.send(f"Here is the Link to invite me to your Server :D\nInvite: https://discord.com/oauth2/authorize?client_id=1236367345656660089&permissions=277025426432&scope=bot")

@bot.command()
async def info(ctx):
    await ctx.send(f"Bot made with :heart: by skumixca\nInvite: https://discord.com/oauth2/authorize?client_id=1236367345656660089&permissions=277025426432&scope=bot")


@bot.command()
async def stats(ctx):
    global image_count, voice_count
    await ctx.send(f"Images generated: {image_count}\nVoice files generated: {voice_count}\nText Messages generated: {text_count}")

bot.run(os.environ.get("token"))
