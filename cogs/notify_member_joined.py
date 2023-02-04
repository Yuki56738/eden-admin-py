from discord import *
from google.cloud import firestore

db = firestore.Client()
class NotifyMemberJoined(Cog):
    def __init__(self, bot):
        self.bot = bot

        # self._last_member = None
    @Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        global db
        guilddbRef = db.collection(str(member.guild.id)).document('settings')
        notify_channel_id = guilddbRef.get().to_dict().get('notify_member_joined_channel')
        if before.channel != after.channel:
            # 通知メッセージを書き込むテキストチャンネル（チャンネルIDを指定）
            botRoom = self.bot.get_channel(int(notify_channel_id))

            # 入退室を監視する対象のボイスチャンネル（チャンネルIDを指定）
            # announceChannelIds = [bbbbbbbbbbbbbbbbbb, cccccccccccccccccc]

            # 退室通知
            if before.channel is not None:
                await botRoom.send("**" + before.channel.name + "** から、__" + member.name + "__  が抜けました！")
            # 入室通知
            if after.channel is not None:
                await botRoom.send("**" + after.channel.name + "** に、__" + member.name + "__  が参加しました！")
        # if notify_channel_id is None:
            # guilddbRef.create({})
    @Cog.listener()
    async def on_ready(self):
        print("ready.")
def setup(bot):
    bot.add_cog(NotifyMemberJoined(bot))