import re
import sys
import os
from dotenv import load_dotenv
import discord
from discord import *

load_dotenv()
TOKEN = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

vcRole = {}
vcTxt = {}


@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user}")
    # bot.activity = "Created by Yuki."
    await bot.change_presence(activity=Game(name="Created by Yuki."))


@bot.event
async def on_reaction_add(reaction: Reaction, user: User):
    print(reaction.message.author)
    print(user.name)

    txt2 = bot.get_channel(1024881096518803466)
    if reaction.message.channel.id == 1021255885542137939:
        await txt2.send(f"{user.mention} から {reaction.message.author.mention} へ募集がありました！")


@bot.event
async def on_message(message: Message):
    if message.author.bot:
        return
    if message.content.startswith("y.help"):
        msgToSend = Embed(title="Yukiの管理BOT", description="y.show または my.show -> 自分の自己紹介を表示する。")
        await message.channel.send(embed=msgToSend, delete_after=3 * 60)
    if message.content.startswith(".debug"):
        print(f"vcRole: {vcRole}")
        print(f"vcTxt: {vcTxt}")
    if message.content.startswith("y.ren"):
        msg = message.content
        msg = re.sub("y.ren ", "", msg)
        try:
            txt1 = vcTxt.get(message.author.voice.channel.id)
            txt1 = bot.get_channel(txt1)
        except:
            return
        await txt1.edit(name=msg)
        vc1 = message.author.voice.channel
        await vc1.edit(name=msg)
        return
    if message.content.startswith("y.show") or message.content.startswith("my.show"):
        msg = message.content
        msg = re.sub("y.show ", "", msg)
        prof_channel = bot.get_channel(995656569301774456)
        prof_messages = await prof_channel.history(limit=1000).flatten()
        # print(prof_messages)
        # for xuser in message.author.voice.channel.members:
        # msgToSend = ""
        for x in prof_messages:
            # if x.author.id == xuser.id:
            if x.author.id == message.author.id:
                await message.channel.send(x.content, delete_after=3 * 60)
                print(f"{x.author.name}: {x.content}")
            if msg in x.author.name:
                print(f"{x.author.name}: {x.content}")
            try:
                for xuser in message.author.voice.channel.members:
                    if x.author.id == xuser.id:
                        print(x.content)
            except:
                pass
        return
    if message.content.startswith("y.lim"):
        msg = message.content
        msg = re.sub("y.lim ", "", msg)
        try:
            txt1 = vcTxt.get(message.author.voice.channel.id)
            txt1 = bot.get_channel(txt1)
        except:
            return
        await message.author.voice.channel.edit(user_limit=int(msg))


@bot.event
async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState):
    # print("hit.")
    print(before.channel)
    print(after.channel)
    if not member.guild.id == 994483180927201400:
        return
    if before.channel is None:
        if after.channel.id == 1019948085876629516:
            print("hit.")
            # await member.guild.system_channel.send("hit.")
            role1 = await member.guild.create_role(name=f"{member.name}の部屋")
            # perm1 = PermissionOverwrite().from_pair(Permissions.general(), Permissions.none())
            perm1 = PermissionOverwrite().from_pair(Permissions.all(), Permissions.none())
            vc1 = await member.guild.create_voice_channel(f"{member.name}の部屋", overwrites={role1: perm1,
                                                                                             member.guild.default_role: PermissionOverwrite().from_pair(
                                                                                                 Permissions.general(),
                                                                                                 Permissions.text())},
                                                          category=bot.get_channel(1012943676332331118))
            vcRole[vc1.id] = role1.id
            print(vcRole)
            await member.add_roles(role1)
            await member.move_to(vc1)
            txt1 = await member.guild.create_text_channel(name=f"{member.name}の部屋", overwrites={role1: perm1,
                                                                                                  member.guild.default_role: PermissionOverwrite().from_pair(
                                                                                                      Permissions.none(),
                                                                                                      Permissions.all())},
                                                          category=bot.get_channel(1012943676332331118))
            vcTxt[vc1.id] = txt1.id
            print(after.channel.members)
            print(len(after.channel.members))
            msgToSend = """y.ren [名前] で部屋の名前を変える
            例｜y.ren 私のおうち
            y.lim [人数] で部屋の人数制限を変える
            例｜y.lim 4（半角
            y.del でチャンネルを削除"""
            await txt1.send(msgToSend)

            try:
                prof_channel = bot.get_channel(995656569301774456)
                prof_messages = await prof_channel.history(limit=1000).flatten()
                print(prof_messages)
                for x in prof_messages:
                    if x.author.id == member.id:
                        await txt1.send(x.content)
            except:
                pass
            return
        role1 = vcRole.get(after.channel.id)
        role1 = member.guild.get_role(role1)
        txt1 = vcTxt.get(after.channel.id)
        txt1 = bot.get_channel(txt1)
        await member.add_roles(role1)
        prof_channel = bot.get_channel(995656569301774456)
        prof_messages = await prof_channel.history(limit=1000).flatten()
        print(prof_messages)
        for x in prof_messages:
            if x.author.id == member.id:
                await txt1.send(x.content)

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


bot.run(TOKEN)
