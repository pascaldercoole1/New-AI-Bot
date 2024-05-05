import discord
from discord.ext import commands
import os
from leptonai.client import Client
from keep_alive import keep_alive
import random
import time
import datetime

# Global variables to track statistics
image_count = 0
voice_count = 0
start_time = time.time()

# Set up Lepton AI client
api_token = os.environ.get('api')
lepton_client = Client("https://sdxl.lepton.run", token=api_token)

# Discord bot setup
intents = discord.Intents.default()
intents.messages = True  # Enable message-related events
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
        untere_grenze = 1009774958
        obere_grenze = 4809774958
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

        # Upload image to Discord
        await ctx.send(file=discord.File(f'output_image_{str(zufallszahl)}.png'))
        os.remove(f'output_image_{str(zufallszahl)}.png')  # Remove the file after uploading
        
        # Increment image count
        image_count += 1
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command()
async def voice(ctx, *, prompt):
    global voice_count
    try:
        c = Client("https://openvoice.lepton.run", token=api_token)
        
        untere_grenze = 1009774958
        obere_grenze = 4809774958
        zufallszahl = random.randint(untere_grenze, obere_grenze)

        mpeg=c.run(
            reference_speaker="https://www.lepton.ai/playground/openvoice/inputs/speaker_1.mp3",
            text=prompt,
            emotion="friendly"
        )
        with open(f'output_image_{zufallszahl}.mp3', 'wb') as f:
            f.write(mpeg)

        # Upload image to Discord
        await ctx.send(file=discord.File(f'output_image_{zufallszahl}.mp3'))
        os.remove(f'output_image_{zufallszahl}.mp3')  # Remove the file after uploading
        
        # Increment voice count
        voice_count += 1
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command()
async def uptime(ctx):
    global start_time
    current_time = time.time()
    uptime_seconds = int(current_time - start_time)
    uptime_string = str(datetime.timedelta(seconds=uptime_seconds))
    await ctx.send(f"Uptime: {uptime_string}")

@bot.command()
async def stats(ctx):
    global image_count, voice_count
    await ctx.send(f"Images generated: {image_count}\nVoice files generated: {voice_count}")

# Run the bot
bot.run(os.environ.get("token"))
