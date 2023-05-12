from google.cloud import firestore
from google.cloud.firestore import *
import discord
from discord.ui import *
from discord import *

db = firestore.Client()
bot_author_id = 451028171131977738

class setvar(Cog):


    @commands.slash_command(description='設定を表示する。')
    async def printvar(self, ctx: ApplicationContext):
        global db
        docs = db.collection(str(ctx.guild.id))
        for x in docs.get():
            x:DocumentSnapshot
            if not x == '':
                await ctx.channel.send(str(x))

            print(x.to_dict())

    @commands.slash_command(description='設定する。')
    async def setvar(self, ctx: ApplicationContext, varname:str, payload:str):
        # x =
        await ctx.respond('setvar hit')
        # await
        global db
        docref = db.collection(str(ctx.guild.id)).document('settings')
        await docref.set(document_data={varname: payload})

    # async def move(self, ctx: ApplicationContext):
        # await ctx.respond(view=MyViewMoveMember())
    @Cog.listener()
    async def on_ready(self):
        print("setvar ready.")
def setup(bot):
    bot.add_cog(setvar(bot))

