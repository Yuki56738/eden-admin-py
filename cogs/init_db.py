from discord import *
from google.cloud import firestore
# from firestore import *

class Init_db(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def init_db(self, ctx: ApplicationContext, *, args: Option(required=False)):
        print("init_db hit.")
        if not ctx.user.guild_permissions.administrator:
            await ctx.respond("あなたは管理者ではありません！")
            return
        # print(args)
        # await ctx.respond(args)
        await ctx.respond("頑張っています...")
        db = firestore.Client()
        guildcol = db.collection("guilddb")
        guildsettingsDoc_ref = guildcol.document("guildsettings")
        guildcol1 = guildsettingsDoc_ref.collection(str(ctx.guild_id))
        # guildcol1: Reference
        # guildcol1.get()
        # guildcol1_payload: Collection = guildcol1.get()
        # guildcol1_payload.save()
        guildcol1: firestore.CollectionReference
        guildcol1Doc = guildcol1.document(document_id=str(ctx.guild_id))
        await ctx.respond("Done.")
        print(guildcol1Doc.get().to_dict())
        if guildcol1Doc.get().to_dict() is None:
            guildcol1Doc.create(document_data={})
        await ctx.send(guildcol1Doc.get().to_dict())
        await ctx.send("Setting data to DB...")
        guildcol1Doc.set(document_data={
            "name": str(ctx.guild.name)
        })
        await ctx.send(guildcol1Doc.get().to_dict())
        guildcol1Doc.update({
            "id": str(ctx.guild_id)
        })
        await ctx.send(guildcol1Doc.get().to_dict())

        # print(guildsettingsDoc.to_dict())
        # await ctx.send(guildsettingsDoc.to_dict())
    # @commands.slash_command()
    # async def list_db(self, ctx: ApplicationContext):
    #     await ctx.respond("頑張っています...")
    #     db = firestore.Client()
    #     guilddbCol = db.collection("guilddb")
    #     guildsettingsCol = db.collection("guildsettings")
    #     await ctx.respond(list(guildsettingsCol.list_documents()))
def setup(bot: Bot):
    bot.add_cog(Init_db(bot))