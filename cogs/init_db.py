from discord import *
from google.cloud import firestore
from google.cloud.firestore import *
class init_db(Cog):
    def __init__(self, bot):
        self.bot = bot
        # self._last_member = None

    @Cog.listener()
    async def on_ready(self):
        print("ready.")
    @Cog.listener()
    async def on_message(self, message: Message):
        if '.init1' in message.content:
            if not message.author.guild_permissions.administrator:
                return
            # db = firestore.Client()
            # guilddb = db.collection('guilddb')
            # guildsettings = guilddb.document(str(message.guild.id))
            # print(guildsettings.get().to_dict())

            db = firestore.Client()
            guilddbRef = db.collection(str(message.guild.id)).document('settings')
            print(guilddbRef.update({
                'create_vc_channel': '1019948085876629516',
                'create_qm_general': '1061927542644293682',
                'create_qm_1': '1061931450825449492',
                'create_qm_2': '1061951354957991976',
                'member_role': '997644021067415642',
                'profile_channel': '995656569301774456'
            }))
        if message.content.startswith('.debug'):
            if message.author.guild_permissions.administrator:
                db = firestore.Client()
                guilddbRef = db.collection(str(message.guild.id)).document('settings')
                await message.channel.send(guilddbRef.get().to_dict())
        # db = firestore.Client()
        # guilddb = db.document('guilddb')
        # guilddbColRef: DocumentReference = guilddb.collection(str(ctx.guild.id))
        # guilddbColRef.set()
        # guilddb = db.collection(str(ctx.guild.id))
        # guilddbDoc1 = guilddb.document(document_id='create_vc_channel')
        # guilddbDoc1.set(document_data='1019948085876629516')
        # guildsettings = guilddb.document(str(ctx.guild.id))
        # print(guildsettings.get().to_dict())
        # var1 = guildsettings.update({
        #     'create_vc_channel': '1019948085876629516',
        #     'member_role': '997644021067415642'
        # })
        # print(var1)
        # guildsettingsDoc1 = guildsettings.collection()
        # guildsettingsDoc1 = guildsettings.get()
        # guildsettingsDoc1
def setup(bot):
    bot.add_cog(init_db(bot))
