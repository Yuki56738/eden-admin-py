import os
import traceback

from discord.ext import pages
from dotenv import load_dotenv
# pip3 install py-cord[voice] --pre
import discord
from discord import *
from discord.ext.commands import *
from discord.ext.pages import *

load_dotenv()
TOKEN = os.environ.get("DISCORD_TOKEN")

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user}")

@bot.slash_command()
async def test_pages(ctx: ApplicationContext):
    await ctx.defer()
    test_pages = ['Page-One', 'Page-Two', 'Page-Three', 'Page-Four', 'Page-Five']
    paginator = pages.Paginator(pages=test_pages)
    await paginator.respond(ctx.interaction)

bot.run(TOKEN)