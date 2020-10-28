# welcome bot
import discord
from discord.ext import commands
import random
import os

# load env
TOKEN = os.environ.get('DISCORD_BOT_TOKEN', '')
extensions = ["member"]

# spawn bot
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """Displays information on successful Discord bot connection"""
    print(f"Logged in as '{bot.user.name}'\n")

# run bot
if __name__ == "__main__":
    print("Loading modules...")
    for extension in extensions:
        try:
            bot.load_extension(f'cogs.{extension}')
            print(f"- cogs.{extension}")
        except Exception as e:
            exc = f'{type(e).__name__}: {e}'
            print(f'Failed to load extension {extension}\n{exc}')

    print("\nConnecting to Discord...")
    bot.run(TOKEN) 
