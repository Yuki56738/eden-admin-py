import discord
from discord import *
from discord.ui import *
import libyuki
from google.cloud import firestore
from google.cloud.firestore import *
from discord.commands import *
from discord.interactions import *
import discord.interactions
from discord.ui.view import *
import discord.ui.view


class Move(Cog):
    def __init__(self, bot):
        self.bot = bot

    class MyViewMoveMember(discord.ui.View):
        @discord.ui.user_select(
            placeholder="ユーザーを選択してください",
            min_values=1,
            max_values=1,

        )
        async def select_callback(self, select: Select, interaction: Interaction):
            # global guildsettings
            await interaction.response.send_message(f"頑張っています...")

            # print(select.to_dict())
            print(select.values[0])
            member1: Member = select.values[0]
            member1 = interaction.user
            # memnber1 = bot.get_user(member1)
            guilddb = libyuki.get_guilddb()
            guildsettingsdb: DocumentReference = guilddb.document(document_id="guildsettings").get()

            var1 = guildsettingsdb.to_dict()

            var2 = var1["994483180927201400"]["move_channel"]
            print(var2)
            # member1.move_to()
            # print(toMoveChannel)
            # await inte("移動しています...")
            # await interaction.followup("移動しています...")
            # toMoveChannel1 = Move.move.bot.get_channel(int(var2))
            toMoveChannel1 = interaction.guild.get_channel(var2)
            await interaction.channel.send("移動しています...")
            # toMoveChannel1 = bot.get_channel(int(toMoveChannel))
            await member1.move_to(toMoveChannel1)

    @slash_command()
    async def move(self, ctx: ApplicationContext):
        await ctx.respond(view=Move.MyViewMoveMember())
        # @bot.slash_command(name="move", description="ユーザーを移動させる")
    # async def move(ctx: ApplicationContext):
    #     await ctx.respond(view=MyViewMoveMember())


def setup(bot):
    bot.add_cog(Move(bot))
