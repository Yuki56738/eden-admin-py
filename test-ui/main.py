import discord
from discord.ext import pages
from dotenv import load_dotenv
import os
from discord import *
from discord.ui import *

load_dotenv('../.envDev')

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

    chan = bot.get_channel(1064989376448319612)
    # await chan.send(Message().)
    # await chan.send(Button.from_component(Button(label='aaaa')))
    # button1 = Button(label='aaaaa')
    # discord.ui.Button(custom_id='abcd', label='aaaaa')
    # async def callback():
    #     print(1)

    # await chan.send(View.add_item(Item(Button())))
    # await chan.send(view=MyView())


bot.run(TOKEN)
