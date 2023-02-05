from discord import *


class DelMsgById(Cog):
    def __init__(self, bot):
        self.bot = bot

        # self._last_member = None

    @commands.slash_command(description='指定されたユーザーのメッセージを全て削除する。')
    @commands.option(name='user_id', required=False)
    async def delusermsgbyid(self, ctx: ApplicationContext, user_id: str):
        if not ctx.user.guild_permissions.administrator:
            await ctx.respond('権限拒否.')
            return
        await ctx.respond('頑張っています...')
        self.bot: Bot
        toDeleteember = await self.bot.fetch_user(int(user_id))
        print(toDeleteember.name, toDeleteember.id)
        channs = await ctx.guild.fetch_channels()
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
                if x.author == toDeleteember:
                    print('deleting:', x.content)
                    await x.delete()
        await ctx.followup.send('削除しました。')

    @Cog.listener()
    async def on_ready(self):
        print("DelMsgById ready.")


def setup(bot):
    bot.add_cog(DelMsgById(bot))
