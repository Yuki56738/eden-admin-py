import discord
from discord import *


class DelMsgById(Cog):
    def __init__(self, bot):
        self.bot = bot

        # self._last_member = None

    @commands.slash_command(description='指定されたユーザーのメッセージを全て削除する。')
    @commands.option(name='user_id', required=True, description='削除するユーザーのID')
    @commands.option(name='channel_id', required=False, description='削除対象のチャンネルのID')
    async def delusermsgbyid(self, ctx: ApplicationContext, user_id: str, channel_id: str):
        if not ctx.user.guild_permissions.administrator:
            await ctx.respond('権限拒否.')
            return
        # await ctx.respond('頑張っています...')
        self.bot: Bot
        ctx.followup: Webhook
        # await ctx.user.send(view=self.ModalToConfirmDelete)
        await ctx.send_modal(self.ModalToConfirmDelete(title="Are you sure to do this?"))


        # toDeleteember = await self.bot.fetch_user(int(user_id))
        # print(toDeleteember.name, toDeleteember.id)

        # channs = await ctx.guild.fetch_channels()
        # for chann in channs:
        #     # if not chann is TextChannel:
        #     #     continue
        #     # if chann == TextChannel:
        #     #     print(3)
        #     try:
        #         msgs = await chann.history(limit=10000).flatten()
        #     except:
        #         continue
        #     for x in msgs:
        #         if x.author == toDeleteember:
        #             if channel_id is None:
        #                 print('deleting:', x.content)
        #                 await x.delete()
        #             elif not channel_id is None and int(x.channel.id) == int(channel_id):
        #                 print('deleting at channel:', self.bot.get_channel(int(channel_id)).name)
        #                 print('deleting:', x.content)
        #                 await x.delete()
        # await ctx.followup.send('削除しました。')

    async def executedel(self, ctx: ApplicationContext, user_id:str ,channel_id: str):
        toDeleteember = await self.bot.fetch_user(int(user_id))
        print(toDeleteember.name, toDeleteember.id)
        channs = await ctx.guild.fetch_channels()
        for chann in channs:
            # if not chann is TextChannel:
            #     continue
            # if chann == TextChannel:
            #     print(3)
            try:
                msgs = await chann.history(limit=10000).flatten()
            except:
                continue
            for x in msgs:
                if x.author == toDeleteember:
                    if channel_id is None:
                        print('deleting:', x.content)
                        await x.delete()
                    elif not channel_id is None and int(x.channel.id) == int(channel_id):
                        print('deleting at channel:', self.bot.get_channel(int(channel_id)).name)
                        print('deleting:', x.content)
                        await x.delete()
        await ctx.followup.send('削除しました。')


    @Cog.listener()
    async def on_ready(self):
        print("DelMsgById ready.")
    class ModalToConfirmDelete(discord.ui.Modal):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            self.add_item(discord.ui.InputText(label="Type yes in uppercase..."))
        async def callback(self, interaction: Interaction):
            interaction.response: InteractionResponse
            await interaction.response.send_message("Executing...")
            toDeleteember = await self.bot.fetch_user(int(user_id))
            print(toDeleteember.name, toDeleteember.id)
            channs = await interaction.guild.fetch_channels()
            for chann in channs:
                # if not chann is TextChannel:
                #     continue
                # if chann == TextChannel:
                #     print(3)
                try:
                    msgs = await chann.history(limit=10000).flatten()
                except:
                    continue
                for x in msgs:
                    if x.author == toDeleteember:
                        if channel_id is None:
                            print('deleting:', x.content)
                            await x.delete()
                        elif not channel_id is None and int(x.channel.id) == int(channel_id):
                            print('deleting at channel:', self.bot.get_channel(int(channel_id)).name)
                            print('deleting:', x.content)
                            await x.delete()
            await ctx.followup.send('削除しました。')


def setup(bot):
    bot.add_cog(DelMsgById(bot))
