import discord
from discord.ext import commands
import os
from leptonai.client import Client

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
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def generate(ctx, *, prompt):
    print("HI")
    try:
        image = lepton_client.run(
            prompt=prompt,
            height=1024,
            width=1024,
            guidance_scale=5,
            high_noise_frac=0.75,
            seed=1809774958,
            steps=30,
            use_refiner=False
        )
        with open(f'output_image_{prompt}.png', 'wb') as f:
            f.write(image)

        # Upload image to Discord
        await ctx.send(file=discord.File(f'output_image_{prompt}.png'))
        os.remove(f'output_image_{prompt}.png')  # Remove the file after uploading
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command()
async def voice(ctx, *, prompt):
    print("HI")
    try:
        c = Client("https://openvoice.lepton.run", token=api_token)

        mpeg=c.run(
            reference_speaker="https://www.lepton.ai/playground/openvoice/inputs/speaker_1.mp3",
            text=prompt,
            emotion="friendly"
        )
        with open(f'output_image_{prompt}.mp3', 'wb') as f:
            f.write(mpeg)

        # Upload image to Discord
        await ctx.send(file=discord.File(f'output_image_{prompt}.mp3'))
        os.remove(f'output_image_{prompt}.mp3')  # Remove the file after uploading
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command()
async def generate(ctx, *, prompt):
    print("HI")
    try:
        image = lepton_client.run(
            prompt=prompt,
            height=1024,
            width=1024,
            guidance_scale=5,
            high_noise_frac=0.75,
            seed=1809774958,
            steps=30,
            use_refiner=False
        )
        with open(f'output_image_{prompt}.png', 'wb') as f:
            f.write(image)

        # Upload image to Discord
        await ctx.send(file=discord.File(f'output_image_{prompt}.png'))
        os.remove(f'output_image_{prompt}.png')  # Remove the file after uploading
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

# Run the bot
bot.run(os.environ.get("token"))
