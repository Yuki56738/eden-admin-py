from google.cloud import firestore
from google.cloud.firestore import *
import discord
from discord.ui import *
from discord import *

db = firestore.Client()
bot_author_id = 451028171131977738

class selfintrod(Cog):
    @Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return
        msgauthorroles = message.author.roles
        # flag = False
        hasvillager = False
        villagerrole = 0
        for x in msgauthorroles:
            # print(x.name)
            if '村人' in x.name:
                hasvillager = True
                villagerrole = x
                break
        citizenrole = 0
        for x in message.guild.roles:
            if '市民' in x.name:
                citizenrole = x
        # if message.channel.id == 965426636436697088:
        if hasvillager and message.channel.id == 1107916826924564480:
            print('debug: now to do run some code')
            msg = message.content
            tosendchan = message.guild.get_channel(965426636436697088)
            msg = f"{message.author.mention} さんのプロフ:\n" + msg
            await tosendchan.send(msg)
            await message.delete()
            await message.author.remove_roles(villagerrole)
            await message.author.add_roles(citizenrole)


    # @commands.slash_command
    # async def debug(self, ctx: ApplicationContext):
            # ctx.guild.guild
    @Cog.listener()
    async def on_ready(self):
        print("selfintrod ready.")

def setup(bot):
    bot.add_cog(selfintrod(bot))

