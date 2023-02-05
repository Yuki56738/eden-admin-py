import traceback

from discord import *
from google.cloud import firestore
from google.cloud.firestore import *
import discord
from discord.ui import *

db = firestore.Client()
bot_author_id = 451028171131977738


class MyViewSelectChannel(discord.ui.View):
    # @discord.ui.sel(
    #     placeholder="ユーザーを選択してください",
    #     min_values=1,
    #     max_values=1
    #
    # )
    @discord.ui.select(
        select_type=discord.ComponentType.channel_select,
        placeholder="選択してください...",
        min_values=1,
        max_values=1,
        # channel_select()
    )
    async def select_callback(self, select: Select, interaction: Interaction):
        interaction.response: InteractionResponse
        print(select.values[0])
        # await interaction.response.send_modal()


class init_db(Cog):
    def __init__(self, bot):
        self.bot = bot
        # self._last_member = None

    @commands.slash_command(description='初期化する.')
    @commands.option(name='force', required=False)
    async def initialize(self, ctx: ApplicationContext, force: bool):
        global bot_author_id
        flag = False
        if int(ctx.user.id) == int(bot_author_id):
            flag = True
        print(str(flag))
        if not ctx.user.guild_permissions.administrator and not flag:
            await ctx.respond('権限拒否.')
            return
        await ctx.respond('頑張っています...')
        flag = False
        global db
        guilddbRef = db.collection(str(ctx.guild.id)).document('settings')
        # listen_channel_id = guilddbRef.get().to_dict()['listen_channel']
        # notify_channel_id = guilddbRef.get().to_dict()['notify_channel']
        vcRoleRef = db.collection(str(ctx.guild.id)).document('vcRole')
        if not guilddbRef.get().to_dict() is None and not vcRoleRef.get().to_dict() is None:
            await ctx.followup.send(
                'あれ？すでにデータベースに存在する...?')
            if not force:
                return
        try:
            guilddbRef.create({})
            vcRoleRef.create({})
        except:
            pass
        await ctx.followup.send('データベースを作成しました！\n/init_1 にて、次の設定にお進みください！')

    # @commands.slash_command(description='強制的に初期化する.')
    # async def init_force(self, ctx: ApplicationContext, force: bool):
    #     global bot_author_id
    #     flag = False
    #     if int(ctx.user.id) == int(bot_author_id):
    #         flag = True
    #     print(str(flag))
    #     if not ctx.user.guild_permissions.administrator and not flag:
    #         await ctx.respond('権限拒否.')
    #         return
    #     await ctx.respond('頑張っています...')
    #     flag = False
    #     if force == False:
    #         await ctx.respond('本当に実行するには、force を True にしてください！')
    #         return
    #     await ctx.respond('頑張っています...')
    #     global db
    #     guilddbRef = db.collection(str(ctx.guild.id)).document('settings')
    #     vcRoleRef = db.collection(str(ctx.guild.id)).document('vcRole')
    #     try:
    #         guilddbRef.create({})
    #         vcRoleRef.create({})
    #     except:
    #         traceback.print_exc()
    #     await ctx.followup.send('データベースを作成しました！\n/init_1 にて、次の設定にお進みください！')

    @commands.slash_command(description='寝落ちした人の移動先を指定する.')
    async def init_1(self, ctx: ApplicationContext, channel_id: str):
        global bot_author_id
        flag = False
        if int(ctx.user.id) == int(bot_author_id):
            flag = True
        print(str(flag))
        if not ctx.user.guild_permissions.administrator and not flag:
            await ctx.respond('権限拒否.')
            return
        await ctx.respond('頑張っています...')
        flag = False
        global db
        guilddbRef = db.collection(str(ctx.guild.id)).document('settings')
        move_channel_id = guilddbRef.get().to_dict().get('move_channel')
        # if move_channel_id is None:
        # await ctx.respond(view=MyViewSelectChannel())
        await ctx.respond(f'"{ctx.guild.get_channel(int(channel_id)).name}" を、寝落ちした人の移動先として設定します...')
        var1 = guilddbRef.get().to_dict()
        var1['move_channel'] = channel_id
        var2 = guilddbRef.update(var1)
        await ctx.followup.send(var2)
        await ctx.followup.send('設定完了。 /init_2 を実行してください。')

    @commands.slash_command(description='プロフィールの検索するチャンネルを指定する.')
    async def init_2(self, ctx: ApplicationContext, channel_id: str):
        global bot_author_id
        flag = False
        if int(ctx.user.id) == int(bot_author_id):
            flag = True
        print(str(flag))
        if not ctx.user.guild_permissions.administrator and not flag:
            await ctx.respond('権限拒否.')
            return
        await ctx.respond('頑張っています...')
        flag = False
        global db
        guilddbRef = db.collection(str(ctx.guild.id)).document('settings')
        await ctx.respond(f'"{ctx.guild.get_channel(int(channel_id)).name}" を、プロフィールの検索するチャンネルとして指定します...')
        var1 = guilddbRef.get().to_dict()
        var1['profile_channel'] = channel_id
        var2 = guilddbRef.update(var1)
        await ctx.followup.send(var2)
        await ctx.followup.send('設定完了。/init_3 を実行してください。')

    @commands.slash_command(description='入退出ログを投稿するチャンネルを指定する。')
    async def init_3(self, ctx: ApplicationContext, channel_id: str):
        global bot_author_id
        flag = False
        if int(ctx.user.id) == int(bot_author_id):
            flag = True
        print(str(flag))
        if not ctx.user.guild_permissions.administrator and not flag:
            await ctx.respond('権限拒否.')
            return
        await ctx.respond('頑張っています...')

        flag = False
        global db
        guilddbRef = db.collection(str(ctx.guild.id)).document('settings')
        var1 = guilddbRef.get().to_dict()
        var1['notify_member_joined_channel'] = channel_id
        var2 = guilddbRef.update(var1)
        await ctx.followup.send(str(var2))
        await ctx.followup.send('設定完了. /init_4 を実行してください！')

    @commands.slash_command(description='サーバーからの退出を通知するチャンネルを指定する。')
    async def init_4(self, ctx: ApplicationContext, channel_id: str):
        global bot_author_id
        flag = False
        if int(ctx.user.id) == int(bot_author_id):
            flag = True
        print(str(flag))
        if not ctx.user.guild_permissions.administrator and not flag:
            flag = False
            await ctx.respond('権限拒否.')
            return
        flag = False
        await ctx.respond('頑張っています...')
        global db
        guilddbRef = db.collection(str(ctx.guild.id)).document('settings')
        # notify_channel_id = guilddbRef.get().to_dict().get('notify_member_joined_channel')
        var1 = guilddbRef.get().to_dict()
        var1['notify_member_leave_channel'] = channel_id
        var2 = guilddbRef.update(var1)
        await ctx.followup.send(var2)
        await ctx.followup.send('設定完了.')

    @Cog.listener()
    async def on_ready(self):
        print("init_db ready.")

    @Cog.listener()
    async def on_guild_join(self, guild: Guild):
        print('Joined to:', guild.name)
        await guild.system_channel.send('こんにちは。Yuki\'s 管理BOTです！\n/initialize にて初期化してください！')
    # @Cog.listener()


def setup(bot):
    bot.add_cog(init_db(bot))
