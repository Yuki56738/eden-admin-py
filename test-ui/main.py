import discord
from discord.ext import pages
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.environ.get("DISCORD_TOKEN")

bot = discord.Bot()


class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Long Input", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Modal Results")
        embed.add_field(name="Long Input", value=self.children[0].value)
        await interaction.response.send_message(embeds=[embed])


class MyViewChangeRoomName(discord.ui.View):
    @discord.ui.button(label="部屋の名前を変える.")
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(MyModal(title="部屋の名前を入力..."))


@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user}")

    chan = bot.get_channel(977138017095520259)
    await chan.send(view=MyView())


bot.run(TOKEN)
