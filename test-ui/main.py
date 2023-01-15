import discord
from discord.ext import pages
from dotenv import load_dotenv
import os
from discord import *
from discord.ui import *

load_dotenv()

TOKEN = os.environ.get("DISCORD_TOKEN")

bot = discord.Bot()


class MyView(discord.ui.View):
    @discord.ui.user_select(
        placeholder="ユーザーを選択してください",
        min_values=1,
        max_values=1,

    )
    async def select_callback(self, select: Select, interaction: Interaction):
        await interaction.response.send_message(f"頑張っています...")
        # print(select.to_dict())
        print(select.values[0])
        member1: Member = select.values[0]


@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user}")

    chan = bot.get_channel(977138017095520259)
    await chan.send(view=MyView())


bot.run(TOKEN)
