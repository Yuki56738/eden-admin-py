# from discord import *
# from google.cloud import firestore
# from firestore import *
#
#
# class Ticket(Cog):
#     def __init__(self, bot):
#         self.bot = bot
#     @Cog.listener()
#     async def on_ready(self):
#         print("ready ticket.")
#
#         # guildsettingsDoc.collection(collection_id=str())
#     @commands.slash_command(description="ticketのDBを初期化")
#     async def init_ticket(self, ctx: ApplicationContext):
#         if not ctx.user.guild_permissions.administrator:
#             await ctx.respond("管理者のみ使用できます.")
#             return
#         db = firestore.Client()
#         guilddbCol = db.collection("guilddb")
#         guildsettingsDoc = guilddbCol.document(document_id="guildsettings")
#         thisGuildCol: Reference = guildsettingsDoc.collection(collection_id=str(ctx.guild_id))
#         # thisGuildCol:
#         # thisGuildCol1 = thisGuildCol
#         # print(type(thisGuildCol))
#         thisGuildCol
# def setup(bot):
#     bot.add_cog(Ticket(bot))

from google.cloud import firestore
from google.cloud.firestore import *
import discord
from discord import *




class Ticket(Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
    @Cog.listener()
    async def on_ready(self):
        print("ready ticket.")

        # guildsettingsDoc.collection(collection_id=str())
    @commands.slash_command(description="ticketのDBを初期化")
    async def init_ticket(self, ctx: ApplicationContext, ticket_channel_id: str):
        if not ctx.user.guild_permissions.administrator:
            await ctx.respond("管理者のみ使用できます.")
            return
        db = firestore.Client()
        guilddbCol = db.collection("guilddb")
        guildsettingsDoc_ref = guilddbCol.document("guildsettings")
        thisguildCol_ref: CollectionReference = guildsettingsDoc_ref.collection(str(ctx.guild.id))

        thisguildDoc = thisguildCol_ref.document(document_id="ticket_channel")
        print(thisguildDoc.get().to_dict())
        thisguildDoc.set({
            "id": str(ctx.guild.get_channel(int(ticket_channel_id)).id),
            "name": str(ctx.guild.get_channel(int(ticket_channel_id)).name)
        })

def setup(bot):
    bot.add_cog(Ticket(bot))


