from discord import *
from google.cloud import firestore
db = firestore.Client()

class NotifyMemeberLeftGuild(Cog):
    def __init__(self, bot):
        self.bot = bot

        # self._last_member = None
    @Cog.listener()
    async def on_member_remove(self, member: Member):
        global db
        guilddbRef = db.collection(str(member.guild.id)).document('settings')
        notify_channel_id = guilddbRef.get().to_dict().get('notify_member_leave_channel')
        self.bot: Bot
        notify_channel = self.bot.get_channel(int(notify_channel_id))
        await notify_channel.send(f'{member.display_name} ({member.name}) ({str(member.id)}) がサーバーから退出しました。')
    @Cog.listener()
    async def on_ready(self):
        print("NotifyMemeberLeftGuild ready.")
def setup(bot):
    bot.add_cog(NotifyMemeberLeftGuild(bot))

