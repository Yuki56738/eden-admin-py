import traceback

from discord import *
from google.cloud import firestore
from google.cloud.firestore import *

db = firestore.Client()


class init_db(Cog):
    def __init__(self, bot):
        self.bot = bot
        # self._last_member = None

    @commands.slash_command(description='初期化する.')
    async def initialize(self, ctx: ApplicationContext):
        if not ctx.user.guild_permissions.administrator:
            await ctx.respond('権限拒否.')
            return
        await ctx.respond('頑張っています...')
        global db
        guilddbRef = db.collection(str(ctx.guild.id)).document('settings')
        # listen_channel_id = guilddbRef.get().to_dict()['listen_channel']
        # notify_channel_id = guilddbRef.get().to_dict()['notify_channel']
        vcRoleRef = db.collection(str(ctx.guild.id)).document('vcRole')
        if not guilddbRef.get().to_dict() is None and not vcRoleRef.get().to_dict() is None:
            await ctx.followup.send(
                'あれ？すでにデータベースに存在する...?\n続行すると、データベースから削除されます！続行するには、/init_force を使用してください！')
            return
        guilddbRef.create({})
        vcRoleRef.create({})
        await ctx.followup.send('データベースを作成しました！\n/init_1 にて、次の設定にお進みください！')

    @commands.slash_command(description='強制的に初期化する.')
    async def init_force(self, ctx: ApplicationContext, force: bool):
        if not ctx.user.guild_permissions.administrator:
            await ctx.respond('権限拒否.')
            return
        if force == False:
            await ctx.respond('本当に実行するには、force を True にしてください！')
            return
        await ctx.respond('頑張っています...')
        global db
        guilddbRef = db.collection(str(ctx.guild.id)).document('settings')
        vcRoleRef = db.collection(str(ctx.guild.id)).document('vcRole')
        try:
            guilddbRef.create({})
            vcRoleRef.create({})
        except:
            traceback.print_exc()
        await ctx.followup.send('データベースを作成しました！\n/init_1 にて、次の設定にお進みください！')
    @Cog.listener()
    async def on_ready(self):
        print("ready.")

    # @Cog.listener()


#     async def on_message(self, message: Message):
#         if '.init1' in message.content:
#             if not message.author.guild_permissions.administrator:
#                 return
#             # db = firestore.Client()
#             # guilddb = db.collection('guilddb')
#             # guildsettings = guilddb.document(str(message.guild.id))
#             # print(guildsettings.get().to_dict())
#
#             db = firestore.Client()
#             guilddbRef = db.collection(str(message.guild.id)).document('settings')
#             # print(guilddbRef.update({
#             #     'create_vc_channel': '1019948085876629516',
#             #     'create_qm_general': '1061927542644293682',
#             #     'create_qm_1': '1061931450825449492',
#             #     'create_qm_2': '1061951354957991976',
#             #     'member_role': '997644021067415642',
#             #     'profile_channel': '995656569301774456'
#             # }))
#             print(guilddbRef.update({
#                 'create_vc_channel': '1064989376905486444',
#                 'create_qm_general': '1064989376645443648',
#                 'create_qm_1': '1064989376645443649',
#                 'create_qm_2': '1064989376645443650',
#                 'member_role': '1064989375613644863',
#                 'profile_channel': '1064989377727569931'
#             }))
#         if message.content.startswith('.init2'):
#             if message.author.guild_permissions.administrator:
#                 db = firestore.Client()
#                 vcRoleRef = db.collection(str(message.guild.id)).document('vcRole')
#                 var1 = vcRoleRef.create({})
#                 print(var1)
#         if message.content.startswith('.update1'):
#             if message.author.guild_permissions.administrator:
#                 db = firestore.Client()
#                 guilddbRef = db.collection(str(message.guild.id)).document('settings')
#                 guilddbRef.update({
#                     'listen_channel': '1021255885542137939',
#                     'notify_channel': '1024881096518803466'
#                 })
#         if message.content.startswith('.update2'):
#             if message.author.guild_permissions.administrator:
#                 db = firestore.Client()
#                 guilddbRef = db.collection(str(message.guild.id)).document('settings')
#                 var2 = guilddbRef.update({
#                     'move_channel': '1064989377165545583'
#                 })
#                 print(var2)
#         if message.content.startswith('.update3'):
#             if message.author.guild_permissions.administrator:
#                 db = firestore.Client()
#                 guilddbRef = db.collection(str(message.guild.id)).document('settings')
#                 var3 = guilddbRef.get().to_dict()
#                 var3.update({
#                     'note_channels': {
#                         '1021255885542137939': '''【 募集する人】
# 〇エロイプや猥談を募集する場合は各目的へ該当するOK女子と男性ロールを使う事。
# 〇深夜に募集を行う場合は必ず深夜メンション可能を使う事。
# 〇趣味の募集を行う時も該当するロールをメンションする事。
# 〇募集をする場合は具体的な時間と日程を書くかすり合わせと書くこと。（今からは書かない事！、余裕をもって、前もった時間を提示する事）。
# 〇すり合わせや約束事は【↑返信↑】で連絡を取り行う事。必ず相手と約束して利用。約束していない人の部屋に勝手に入らない！
# ＊相手のロールをよく確認して募集内容を決める、返信でメンションされた人だけが、システム上部屋に入れます。
# ＊テンプレートに従い！（【 募集 】のピン留めを確認）、 メンションを指定すること！
# ＊ 募集が終わったら必ず削除
# ＊ @everyone @hereはNG''',
#                         '995656569301774456': '''【 名前／年齢／性別 】　　　　　
# 【 趣味／好きな話題 】
# 【 診断結果(MBTI) 】
# 【 サーバを知った場所 】
# 【 ボイスチャットに参加できる時間帯 】
# 【一言】''',
#                         '996367967925305464': '''頭に思い浮かぶ言葉を呟こう！猥談・規約違反、ネガティブ発言、不穏な投稿、政治、宗教、国際情勢やセンシティブな話も禁止とします。なお、会話が盛り上がる場合は返信は良しとしますが、できれば チャット等で話しましょう。''',
#                         '1009439576537968670': ''''●当サーバーではリアルでの出会いは禁止されてます（身バレ等事件性がありますので。）
# ●外部ツールの繋がり等の話題もできる限り避けましょう。
# ●自己防衛やマナーなどに関しては百科事典のガイドラインをご確認ください。
# ＊リアル等で会う発言をされた人や規約違反者は質問＆報告で通報する事。''',
#                         '1008990175583551628': '''●当サーバーではリアルでの出会いは禁止されてます（身バレ等事件性がありますので。）
# ●外部ツールの繋がり等の話題もできる限り避けましょう。
# ●自己防衛やマナーなどに関しては百科事典のガイドラインをご確認ください。
# ＊リアル等で会う発言をされた人や規約違反者は質問＆報告で通報する事。''',
#                         '1008990207187628122': '''●当サーバーではリアルでの出会いは禁止されてます（身バレ等事件性がありますので。）
# ●外部ツールの繋がり等の話題もできる限り避けましょう。
# ●自己防衛やマナーなどに関しては百科事典のガイドラインをご確認ください。
# ＊リアル等で会う発言をされた人や規約違反者は質問＆報告で通報する事。'''
#                     }
#
#                 })
#         # if message.content.startswith('.cleanup_db'):
#         #     if message.author.guild_permissions.administrator:
#         #         db = firestore.Client()
#         #         vcRoleRef = db.collection(str(message.guild.id)).document('vcRole')
#         # vcRoleRef.get().to_dict().pop()
#         if message.content.startswith('.update4'):
#             if message.author.guild_permissions.administrator:
#                 db = firestore.Client()
#                 guilddbRef = db.collection(str(message.guild.id)).document('settings')
#                 var3 = guilddbRef.update({
#                     'move_channel': '996369129508450344'
#                 })
#                 await message.reply(str(var3))
#         if message.content.startswith('.update5'):
#             if message.author.guild_permissions.administrator:
#                 db = firestore.Client()
#                 guilddbRef = db.collection(str(message.guild.id)).document('settings')
#                 # guilddbRef.get(
#                 # var5 = guilddbRef.get().to_dict()
# #                 var5.update({
# #                     'note_channels': {
# #                         '1016234230549843979': '''【名前／年齢 ／性別 】／／
# # 【 対象／好み 】例：女性／カワボ／／
# # 【属性 】例：S,M、ノーマル、スイッチャー
# # 【 好きなプレイ 】例：イチャ甘／／
# # 【 嫌いなプレイ 】例：バチボコ／／
# # 【 寝落ちの可否 】
# # 【 公開 ／複数 】例：OK／複数は女性のみ
# # 【ＰＲ】''',
# #                         '1017679165945819146': '''頭に思い浮かぶ下ネタを呟こう！規約違反、ネガティブ発言、不穏な投稿、政治、宗教、国際情勢やセンシティブな話も禁止。会話が盛り上がる場合はできれば 【🔞 チャット】等で話しましょう。 '''
# #                     }
# #                 })
#                 # print(var5)
#                 # var6 = guilddbRef.update(var5)
#                 await message.reply(str(var6))
#         if message.content.startswith('.debug'):
#             if message.author.guild_permissions.administrator:
#                 db = firestore.Client()
#                 guilddbRef = db.collection(str(message.guild.id)).document('settings')
#                 await message.channel.send(guilddbRef.path)
#                 await message.channel.send(guilddbRef.get().to_dict())
#                 vcRoleRef = db.collection(str(message.guild.id)).document('vcRole')
#                 await message.channel.send(vcRoleRef.path)
#                 await message.channel.send(vcRoleRef.get().to_dict())
#         # db = firestore.Client()
#         # guilddb = db.document('guilddb')
#         # guilddbColRef: DocumentReference = guilddb.collection(str(ctx.guild.id))
#         # guilddbColRef.set()
#         # guilddb = db.collection(str(ctx.guild.id))
#         # guilddbDoc1 = guilddb.document(document_id='create_vc_channel')
#         # guilddbDoc1.set(document_data='1019948085876629516')
#         # guildsettings = guilddb.document(str(ctx.guild.id))
#         # print(guildsettings.get().to_dict())
#         # var1 = guildsettings.update({
#         #     'create_vc_channel': '1019948085876629516',
#         #     'member_role': '997644021067415642'
#         # })
#         # print(var1)
#         # guildsettingsDoc1 = guildsettings.collection()
#         # guildsettingsDoc1 = guildsettings.get()
#         # guildsettingsDoc1


def setup(bot):
    bot.add_cog(init_db(bot))
