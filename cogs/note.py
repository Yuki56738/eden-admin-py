from discord import *
from google.cloud import firestore


class Note(Cog):
    def __init__(self, bot):
        self.bot = bot
        # self._last_member = None
    # @commands.slash_command(description='投稿するnoteを作成する')
    # async def setnote(self, ctx: ApplicationContext, notechannelid: str, value: str):
    #     db = firestore.Client()
    #     guilddbRef = db.collection(str(message.guild.id)).document('settings')
        # try:
        # toSendMsg = guilddbRef.get().to_dict()['note_channels'][str(message.channel.id)]
        # except:
            # return
        # guilddbRef.collection('note_')

    @Cog.listener()
    async def on_ready(self):
        print("note ready.")
    @Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return
        db = firestore.Client()
        guilddbRef = db.collection(str(message.guild.id)).document('settings')
        try:
            toSendMsg = guilddbRef.get().to_dict()['note_channels'][str(message.channel.id)]
        except:
            return
        if toSendMsg is None:
           return
        var1 = await message.channel.history(limit=15).flatten()
        sentTxt1 = await message.channel.send(embed=Embed(description=toSendMsg))

        self.bot: Bot
        for x in var1:
            if x.author.id == self.bot.user.id:
                await x.delete()

                # return
            # break
                # return
                # break
                # break

def setup(bot):
    bot.add_cog(Note(bot))
