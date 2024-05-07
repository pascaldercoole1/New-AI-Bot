import discord
from discord.ext import commands
import os
from leptonai.client import Client
from keep_alive import keep_alive
import random
import time
import datetime
import openai

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
    await ctx.send(f"Images generated: {image_count}\nVoice files generated: {voice_count}\Text Messages generated: {text_count}")

bot.run(os.environ.get("token"))
