import discord
from discord import *

# from discord.commands import *
flag = False
flag2 = False
toDeleteMember = 0


class DelMessages(Cog):
    def __init__(self, bot):
        self.bot = bot

        # self._last_member = None

    @commands.slash_command(description='メンションされたユーザーのメッセージを全て削除する。')
    async def delusermsg(self, ctx: ApplicationContext):
        if not ctx.user.guild_permissions.administrator:
            await ctx.respond('権限拒否.')
            return
        await ctx.respond('頑張っています...')
        await ctx.followup.send(f'{ctx.user.mention} 相手をメンションすると、相手の全てのメッセージが削除されます！\nメンションしてください...')
        global flag
        flag = True

    @Cog.listener()
    async def on_message(self, message: Message):
        global flag
        global flag2
        global toDeleteMember
        if flag:
            flag = False
            if not message.author.guild_permissions.administrator:
                await message.reply('権限拒否.')
                return
            if not message.mentions:
                return
            # await message.reply(str(message.mentions))
            for memb in message.mentions:
                break
            toDeleteMember = memb
            await message.reply(f'{memb.name}さん ({memb.display_name}) さんのメッセージを削除します。\n本当に実行しますか？[!YES/n]')
            flag2 = True
            return
        if flag2:
            flag2 = False
            if message.content == '!YES':
                if not message.author.guild_permissions.administrator:
                    await message.reply('権限拒否.')
                    return
                print('deleting:', toDeleteMember.name, toDeleteMember.id)
                channs = await message.guild.fetch_channels()
                for chann in channs:
                    # if not chann is TextChannel:
                    #     continue
                    # if chann == TextChannel:
                    #     print(3)
                    try:
                        msgs = await chann.history(limit=1000).flatten()
                    except:
                        continue
                    for x in msgs:
                        if x.author.id == toDeleteMember.id:
                            print('deleting...:', x.author.name, x.content)
                            await x.delete()
                await message.reply('削除しました。')
                # print(x.author.name)
                # if chann is TextChannel:
                #     print(2)
                # toDeleteMsgs = await toDeleteMember.history().flatten()
                # for x in toDeleteMsgs:
                #     print(x)
                #     await message.reply(str(x))
            # channels = await message.guild.fetch_channels()

    @Cog.listener()
    async def on_ready(self):
        print("DelMessages ready.")


def setup(bot):
    bot.add_cog(DelMessages(bot))
