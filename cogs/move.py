import discord
from discord import *
from discord.ui import *
# import libyuki
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
        # self.db = firestore.Client()

    class MyViewMoveMember(discord.ui.View):
        # @discord.ui.sel(
        #     placeholder="ユーザーを選択してください",
        #     min_values=1,
        #     max_values=1
        #
         # )
        @discord.ui.select(
            select_type=discord.ComponentType.user_select,
            placeholder="選択してください...",
            min_values=1,
            max_values=1
        )
        async def select_callback(self, select: Select, interaction: Interaction):
            # global guildsettings
            await interaction.response.send_message(f"頑張っています...")

            # print(select.to_dict())
            # print(select.values[0])
            print("select.values[0]", select.values[0])
            member1: Member= select.values[0]
            # member1 = interaction.guild.get_member(member1_id)
            # member1 = interaction.guild.get_member(member1_id)
            # member1 = interaction.guild.get_member(member1)
            # memnber1 = bot.get_user(member1)
            # guilddb = libyuki.get_guilddb()
            # guildsettingsdb: DocumentReference = guilddb.document(document_id="guildsettings").get()
            #
            # var1 = guildsettingsdb.to_dict()
            db = firestore.Client()
            guilddbRef = db.collection(str(interaction.guild.id)).document('settings')
            print(guilddbRef.get().to_dict())
            var1 = guilddbRef.get().to_dict()['move_channel']
            print('var1:',var1)
            # var2 = guilddbRef["994483180927201400"]["move_channel"]
            # print(var2)
            # member1.move_to()
            # print(toMoveChannel)
            # await inte("移動しています...")
            # await interaction.followup("移動しています...")
            # toMoveChannel1 = Move.move.bot.get_channel(int(var2))
            toMoveChannel1 = interaction.guild.get_channel(int(var1))
            await interaction.channel.send("移動しています...")
            # toMoveChannel1 = bot.get_channel(int(toMoveChannel))
            await member1.move_to(toMoveChannel1)

    @slash_command(description="寝落ちした人を移動させる")
    async def move(self, ctx: ApplicationContext):
        await ctx.respond(view=Move.MyViewMoveMember())
        # @bot.slash_command(name="move", description="ユーザーを移動させる")
    # async def move(ctx: ApplicationContext):
    #     await ctx.respond(view=MyViewMoveMember())


def setup(bot):
    bot.add_cog(Move(bot))
