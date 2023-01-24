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
        if '.debug' in message.content:
            db = firestore.Client()
            guilddb = db.collection('guilddb')
            guildsettings = guilddb.document(str(message.guild.id))
            print(guildsettings.get().to_dict())
    @commands.slash_command()
    async def init_db(self, ctx: ApplicationContext):
        if not ctx.user.guild_permissions.administrator:
            await ctx.respond('あなたは管理者ではありません!')
            return
        db = firestore.Client()
        guilddb = db.collection('guilddb')
        guildsettings = guilddb.document(str(ctx.guild.id))
        print(guildsettings.get().to_dict())
        var1 = guildsettings.update({
            'create_vc_channel': 1019948085876629516,
            'member_role': 997644021067415642
        })
        print(var1)
        # guildsettingsDoc1 = guildsettings.collection()
        # guildsettingsDoc1 = guildsettings.get()
        # guildsettingsDoc1
def setup(bot):
    bot.add_cog(init_db(bot))
