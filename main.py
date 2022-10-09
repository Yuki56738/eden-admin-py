import re
import sys
import os
from dotenv import load_dotenv
import discord
from discord import *

# load_dotenv()
# TOKEN = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

vcRole = {}
vcTxt = {}


@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user}")


@bot.event
async def on_message(message: Message):
    if message.content.startswith(".debug"):
        print(f"vcRole: {vcRole}")
        print(f"vcTxt: {vcTxt}")
    if message.content.startswith("y.ren"):
        msg = message.content
        msg = re.sub("y.ren ", "", msg)
        txt1 = vcTxt.get(message.author.voice.channel.id)
        txt1 = bot.get_channel(txt1)
        await txt1.edit(name=msg)
        vc1 = message.author.voice.channel
        await vc1.edit(name=msg)
        return
    if message.content.startswith("y.show"):
        msg = message.content
        prof_channel = bot.get_channel(1018726552936128553)
        prof_messages = await prof_channel.history(limit=1000).flatten()
        print(prof_messages)
        for x in prof_messages:
            if x.author.id == message.author.id:
                await message.channel.send(x.content)
        return
    if message.content.startswith("y.lim"):
        msg = message.content
        msg = re.sub("y.lim ", "", msg)
        await message.author.voice.channel.edit(user_limit=int(msg))


@bot.event
async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState):
    # print("hit.")
    print(before.channel)
    print(after.channel)
    if not member.guild.id == 977138017095520256:
        return
    if before.channel is None:
        if after.channel.id == 1028601419131002930:
            print("hit.")
            # await member.guild.system_channel.send("hit.")
            role1 = await member.guild.create_role(name=f"{member.name}の部屋")
            # perm1 = PermissionOverwrite().from_pair(Permissions.general(), Permissions.none())
            perm1 = PermissionOverwrite().from_pair(Permissions.all(), Permissions.none())
            vc1 = await member.guild.create_voice_channel(f"{member.name}の部屋", overwrites={role1: perm1, member.guild.default_role: PermissionOverwrite().from_pair(Permissions.general(), Permissions.text())},
                                                          category=bot.get_channel(977138017095520258))
            vcRole[vc1.id] = role1.id
            print(vcRole)
            await member.add_roles(role1)
            await member.move_to(vc1)
            txt1 = await member.guild.create_text_channel(name=f"{member.name}の部屋", overwrites={role1: perm1,
                                                                                                  member.guild.default_role: PermissionOverwrite().from_pair(
                                                                                                      Permissions.none(),
                                                                                                      Permissions.all())},
                                                          category=bot.get_channel(977138017095520258))
            vcTxt[vc1.id] = txt1.id
            print(after.channel.members)
            print(len(after.channel.members))
            return
        role1 = vcRole.get(after.channel.id)
        role1 = member.guild.get_role(role1)
        await member.add_roles(role1)

    if after.channel is None:
        print(before.channel.members)
        print(len(before.channel.members))
        if len(before.channel.members) == 0:
            role1 = vcRole.get(before.channel.id)
            role1 = member.guild.get_role(role1)
            txt1 = vcTxt.get(before.channel.id)
            txt1 = bot.get_channel(txt1)
            await role1.delete()
            await before.channel.delete()
            await txt1.delete()
            vcRole.pop(before.channel.id)
            vcTxt.pop(before.channel.id)


bot.run(sys.argv[1])
