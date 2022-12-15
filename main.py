import asyncio
import re
import sys
import os
import traceback

from dotenv import load_dotenv
import discord
from discord import *
import json

# from discord.ui import *

load_dotenv()
TOKEN = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

vcRole = {}
vcTxt = {}
txtMsg = {}
guildsettings = {}
# guildsettings = {
#     "994483180927201400": {
#         "prof_channel": 995656569301774456,
#         "member_role": 997644021067415642,
#         "create_vc_channel": 1019948085876629516,
#         "vc_category": 1012943676332331118,
#         "mention_channel": 1031256109555666966,
#         "note_channels": {
#             "996367967925305464": """
# 頭に思い浮かぶ言葉を呟こう！猥談・規約違反、ネガティブ発言、不穏な投稿、政治、宗教、国際情勢やセンシティブな話も禁止とします。なお、会話が盛り上がる場合は返信は良しとしますが、できれば 🏢チャット等で話しましょう。"""
#             # "995656569301774456":
#         }
#     },
#     "977138017095520256": {
#         "prof_channel": 1018726552936128553,
#         "member_role": 1028601169498615858,
#         "create_vc_channel": 1028601419131002930,
#         "vc_category": 977138017095520258,
#         "mention_channel": 977138017095520259
#     }
# }

bot_author_id = 451028171131977738
bot_author = bot.get_user(bot_author_id)


@bot.event
async def on_ready():
    global vcRole
    global vcTxt
    global txtMsg
    global guildsettings
    print(f"Logged in as: {bot.user}")
    # bot.activity = "Created by Yuki."
    await bot.change_presence(activity=Game(name="Created by Yuki."))
    try:
        with open("guildsettings.json", "r", encoding="utf8") as f:
            guildsettings = json.load(f)
        with open("txtMsg.json", "r") as f:
            txtMsg = json.load(f)
        with open("vcTxt.json", "r") as f:
            vcTxt = json.load(f)
        with open("vcRole.json", "r") as f:
            vcRole = json.load(f)


    except Exception as e:
        print(traceback.format_exc())
    print("Loaded bot state.")


@bot.event
async def on_raw_reaction_add(reaction: RawReactionActionEvent):
    global vcRole
    global vcTxt
    global txtMsg
    global guildsettings
    print("reaction")
    reaction_channel_id = guildsettings[str(reaction.guild_id)]["reaction_channel"]
    txt2_id = guildsettings[str(reaction.guild_id)]["reaction_notify_channel"]
    txt2 = bot.get_channel(txt2_id)
    msg1 = await reaction.member.guild.get_channel(reaction_channel_id).fetch_message(reaction.message_id)
    if reaction.channel_id == reaction_channel_id:
        await txt2.send(f"{reaction.member.mention} から {msg1.author.mention} へ反応がありました！")


@bot.event
async def on_message(message: Message):
    global vcRole
    global vcTxt
    global txtMsg
    global guildsettings
    if message.author.bot:
        return
    if message.content.startswith("y.help"):
        msgToSend = Embed(title="Yukiの管理BOT", description="y.show または my.show -> 自分の自己紹介を表示する。")
        await message.channel.send(embed=msgToSend, delete_after=3 * 60)
    if message.content.startswith(".debug"):
        print(f"vcRole: {vcRole}")
        print(f"vcTxt: {vcTxt}")
    """
    if message.content.startswith("y.ren"):
        msg = message.content
        msg = re.sub("y.ren ", "", msg)
        try:
            txt1 = vcTxt.get(str(message.author.voice.channel.id))
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
        # prof_channel = bot.get_channel(995656569301774456)
        prof_channel = bot.get_channel(guildsettings[str(message.guild.id)]["prof_channel"])
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
    """
    isExist = False
    try:
        guildsettings[str(message.guild.id)]["note_channels"][str(message.channel.id)]
        isExist = True
    except Exception as e:
        print(traceback.format_exc())
    if isExist == True:
        try:
            msg1_id = txtMsg[str(message.channel.id)]
            msg1 = await message.channel.fetch_message(msg1_id)
            await msg1.delete()
        except Exception as e:
            print(traceback.format_exc())
        tosendtxt = guildsettings[str(message.guild.id)]["note_channels"][str(message.channel.id)]
        msg2 = await message.channel.send(embed=Embed(description=tosendtxt))
        txtMsg[str(message.channel.id)] = msg2.id
        save_to_json()
    #     if message.channel.id == 996367967925305464:
    #         # try:
    #         msg1_id = int(0)
    #         try:
    #             msg1_id = txtMsg[str(message.channel.id)]
    #             msg1 = await message.channel.fetch_message(msg1_id)
    #             await msg1.delete()
    #         except:
    #             pass
    #         # except:
    #         #     pass
    #         msg2 = await message.channel.send(embed=Embed(description="""
    # 頭に思い浮かぶ言葉を呟こう！猥談・規約違反、ネガティブ発言、不穏な投稿、政治、宗教、国際情勢やセンシティブな話も禁止とします。なお、会話が盛り上がる場合は返信は良しとしますが、できれば 🏢チャット等で話しましょう。"""))
    #         txtMsg[str(str(message.channel.id))] = msg2.id
    #         save_to_json()
    #     if message.channel.id == 995656569301774456:
    #         try:
    #             msg1_id = txtMsg[str(message.channel.id)]
    #             msg1 = await message.channel.fetch_message(msg1_id)
    #             await msg1.delete()
    #         except:
    #             pass
    #         msg3 = await message.channel.send(embed=Embed(description="""
    # 【 名前／年齢／性別 】　　　　　
    # 【 趣味／好きな話題 】
    # 【 診断結果(MBTI) 】
    # 【 サーバを知った場所 】
    # 【 ボイスチャットに参加できる時間帯 】
    # 【一言】"""))
    #         txtMsg[str(995656569301774456)] = msg3.id
    #         save_to_json()
    #     if message.channel.id == 1016234230549843979:
    #         try:
    #             msg4_id = txtMsg[str(message.channel.id)]
    #             msg4 = await message.channel.fetch_message(msg4_id)
    #             await msg4.delete()
    #         except:
    #             pass
    #         msg2 = await message.channel.send(embed=Embed(description="""
    # 【 名前／年齢 ／性別 】／／
    # 【 対象／好み 】例：女性／カワボ／／
    # 【 S or M 】
    # 【 好きなプレイ 】例：イチャ甘／／
    # 【 嫌いなプレイ 】例：バチボコ／／
    # 【 セーフワード 】例：エンド
    # 【 寝落ちの可否 】
    # 【 公開 ／複数 】例：OK／複数は女性のみ
    # 【ＰＲ】
    # 【 固定について 】・いる or いない
    # 　　　　　　　  　・作りたい or 作りたくない
    # 【 固定の価値観 】例：ネット彼氏、彼女、プレイが好き
    # ―――――――――――――――――
    # ＊固定さん以外との関係　　
    #   【 DM・フレンド申請 】〇 or ✕
    #   【 エロイプ 】〇 or ✕
    #   【 個室の利用 】〇 or ✕"""))
    #         txtMsg[str(message.channel.id)] = msg2.id
    #         save_to_json()
    """
    if message.content.startswith("y.lim"):
        msg = message.content
        msg = re.sub("y.lim ", "", msg)
        try:
            txt1 = vcTxt.get(str(message.author.voice.channel.id))
            txt1 = bot.get_channel(txt1)
        except:
            return
        await message.author.voice.channel.edit(user_limit=int(msg))
    if message.content.startswith("y.save"):
        # await message.guild.system_channel.send("Saving bot state...")
        print("Saving bot state...")
        with open("vcTxt.json", "w") as f:
            # tmpJson:dict = json.load(f)
            json.dump(vcTxt, f)
        with open("vcRole.json", "w") as f:
            json.dump(vcRole, f)
        with open("txtMsg.json", "w") as f:
            json.dump(txtMsg, f)
        print("Saved bot state.")
    if message.content.startswith("y.load"):
        # await message.guild.system_channel.send("Loading bot state...")
        print("Loading bot state...")
        with open("vcTxt.json", "r") as f:
            vcTxt = json.load(f)
        with open("vcRole.json", "r") as f:
            vcRole = json.load(f)
        with open("txtMsg.json", "r") as f:
            txtMsg = json.load(f)
        print("Loaded bot state.")
    if message.content.startswith("y.close"):
        try:
            vcTxt[str(message.author.voice.channel.id)]
        except:
            return
        vc1 = message.author.voice.channel
        role1 = message.guild.get_role(vcRole[str(message.author.voice.channel.id)])
        perm1 = PermissionOverwrite().from_pair(Permissions.advanced().general().voice(), Permissions.none())
        perm2 = PermissionOverwrite().from_pair(Permissions.general(), Permissions.text())
        # perm2.update(connect=True)
        # perm2.update(speak=True)
        # perm2.update(use_slash_commands=True)
        perm2.update(connect=True)
        perm2.update(speak=True)
        # perm1.update(value=689379286592)
        perm1.update(read_message_history=True)
        perm1.update(read_messages=True)
        perm1.update(send_messages=True)
        perm1.update(use_slash_commands=True)
        perm1.update(connect=True, speak=True)
        perms1 = Permissions.advanced().general().voice()
        perm1.update(mute_members=False)
        perm1.update(move_members=False, deafen_members=False)
        perms1.update(mute_members=False, move_members=False, deafen_members=False, connect=True, speak=True)
        # memberRole = message.author.guild.get_role(997644021067415642)
        memberRole = message.guild.get_role(guildsettings[str(message.guild.id)]["member_role"])
        memberPerm = PermissionOverwrite().from_pair(Permissions.advanced().general(), Permissions.all())
        memberPerm.update(view_channel=True)
        await vc1.edit(overwrites={role1: perm1,
                                   memberRole: memberPerm,
                                   message.guild.default_role: PermissionOverwrite().from_pair(
                                       Permissions.none(),
                                       Permissions.all())
                                   }
                       )
        await message.channel.send(embed=Embed(description="完了."))
    """
    if message.mentions:
        try:
            vc1 = message.author.voice.channel
            txt1_id = vcTxt[str(str(vc1.id))]
            txt1 = bot.get_channel(txt1_id)
            perm1 = PermissionOverwrite().from_pair(Permissions.advanced().general().voice(), Permissions.none())
            perm2 = PermissionOverwrite().from_pair(Permissions.general(), Permissions.text())
            # perm2.update(connect=True)
            # perm2.update(speak=True)
            # perm2.update(use_slash_commands=True)
            perm2.update(connect=True)
            perm2.update(speak=True)
            # perm1.update(value=689379286592)
            perm1.update(read_message_history=True)
            perm1.update(read_messages=True)
            perm1.update(send_messages=True)
            perm1.update(use_slash_commands=True)
            perm1.update(connect=True, speak=True)
            perms1 = Permissions.advanced().general().voice()
            perm1.update(mute_members=False)
            perm1.update(move_members=False, deafen_members=False)
            role1 = message.guild.get_role(vcRole[str(vc1.id)])
            if message.channel.id == guildsettings[str(message.guild.id)]["mention_channel"]:
                for x in message.mentions:
                    await x.add_roles(role1)
                    await vc1.edit(overwrites={x: perm1})
        except:
            print(traceback.format_exc())


@bot.event
async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState):
    global vcRole
    global vcTxt
    global txtMsg
    global guildsettings
    try:
        guild1 = guildsettings[str(member.guild.id)]
    except:
        print(traceback.format_exc())

    # if not after.channel is None and after.channel.id == 1019948085876629516:
    if not after.channel is None and after.channel.id == guildsettings[str(member.guild.id)]["create_vc_channel"]:
        print("hit.")
        # await member.guild.system_channel.send("hit.")
        # memberRole = member.guild.get_role(997644021067415642)
        memberRole = member.guild.get_role(guildsettings[str(member.guild.id)]["member_role"])
        # perm1 = PermissionOverwrite().from_pair(Permissions.general(), Permissions.none())
        perm1 = PermissionOverwrite().from_pair(Permissions.advanced().general().voice(), Permissions.none())
        perm2 = PermissionOverwrite().from_pair(Permissions.general(), Permissions.text())
        # perm2.update(connect=True)
        # perm2.update(speak=True)
        # perm2.update(use_slash_commands=True)
        perm2.update(connect=True)
        perm2.update(speak=True)
        # perm1.update(value=689379286592)
        perm1.update(read_message_history=True)
        perm1.update(read_messages=True)
        perm1.update(send_messages=True)
        perm1.update(use_slash_commands=True)
        perm1.update(connect=True, speak=True)
        perms1 = Permissions.advanced().general().voice()
        perm1.update(mute_members=False)
        perm1.update(move_members=False, deafen_members=False, attach_files=True, embed_links=True)
        perms1.update(mute_members=False, move_members=False, deafen_members=False, connect=True, speak=True)
        # perms1.update(connect=True, speak=True)
        role1 = await member.guild.create_role(name=f"{member.display_name}の部屋", permissions=perms1)
        cat1 = bot.get_channel(guildsettings[str(member.guild.id)]["vc_category"])
        vc1 = await member.guild.create_voice_channel(f"{member.display_name}の部屋", overwrites={role1: perm1,
                                                                                                 memberRole: perm2,
                                                                                                 member.guild.default_role: PermissionOverwrite().from_pair(
                                                                                                     Permissions.none(),
                                                                                                     Permissions.all())
                                                                                                 },
                                                      category=cat1, user_limit=2)
        vcRole[str(vc1.id)] = role1.id
        # await role1.edit(position=8)
        await member.add_roles(role1)
        await member.move_to(vc1)
        txt1 = await member.guild.create_text_channel(name=f"{member.display_name}の部屋", overwrites={role1: perm1,
                                                                                                      member.guild.default_role: PermissionOverwrite().from_pair(
                                                                                                          Permissions.none(),
                                                                                                          Permissions.all())},
                                                      category=cat1)
        vcTxt[str(vc1.id)] = txt1.id
        msgToSend = """
Created by Yuki.
/name [名前] で部屋の名前を変える
例｜/name 私のおうち
/limit [人数] で部屋の人数制限を変える
例｜/limit 4（半角
/close でこの部屋に入れる人を限定する。「返信」にてメンションされた人は入れるようになる。
/nolook でこの部屋を見えなくする。
/look で、この部屋を見えるようにする。"""
        await txt1.send(msgToSend)
        try:
            # prof_channel = bot.get_channel(995656569301774456)
            prof_channel_id = guildsettings[str(member.guild.id)]["prof_channel"]
            prof_channel = bot.get_channel(prof_channel_id)
            prof_messages = await prof_channel.history(limit=1000).flatten()
            for x in prof_messages:
                if x.author.id == member.id:
                    await txt1.send(x.content)
        except:
            print(traceback.format_exc())
        await txt1.send(member.mention)
        save_to_json()
        return
    if after.channel != before.channel:
        try:
            role1 = vcRole[str(after.channel.id)]
            role1 = member.guild.get_role(role1)
            txt1 = vcTxt[str(after.channel.id)]

            txt1 = bot.get_channel(txt1)
            await member.add_roles(role1)
            save_to_json()
            # prof_channel = bot.get_channel(995656569301774456)
            prof_channel_id = guildsettings[str(member.guild.id)]["prof_channel"]
            prof_channel = bot.get_channel(prof_channel_id)
            prof_messages = await prof_channel.history(limit=1000).flatten()
            for x in prof_messages:
                if x.author.id == member.id:
                    await txt1.send(x.content)
            await txt1.send(member.mention)
        except:
            print(traceback.format_exc())

    if not before.channel is None and len(before.channel.members) == 0:
        txt1_id = vcTxt[str(before.channel.id)]
        txt1 = bot.get_channel(txt1_id)
        await txt1.delete()
        role1 = vcRole[str(before.channel.id)]
        role1 = member.guild.get_role(role1)
        await role1.delete()
        await before.channel.delete()
        vcRole.pop(str(before.channel.id))
        vcTxt.pop(str(before.channel.id))
        save_to_json()


@bot.slash_command(description="自己紹介を表示")
async def show(ctx: ApplicationContext, name: Option(str, required=True, description="名前")):
    global vcRole
    global vcTxt
    global txtMsg
    global guildsettings
    prof_channel_id = guildsettings[str(ctx.guild.id)]["prof_channel"]
    prof_channel = bot.get_channel(prof_channel_id)
    prof_messages = await prof_channel.history(limit=1000).flatten()
    # await ctx.respond("自己紹介...", ephemeral=True, delete_after=3*60)
    # print(ctx.author.guild_permissions)
    tosendmsg = ""
    for x in prof_messages:
        # if x.author.id == xuser.id:
        if x.author.id == ctx.author.id:
            # await ctx.send_followup(x.content, delete_after=3 * 60, ephemeral=True)
            # tosendmsg = tosendmsg + x.content
            print(f"{x.author.name}: {x.content}")

        # for xuser in ctx.author.voice.channel.members:
        #     if x.author.id == xuser.id and not ctx.author.id:
        #         print(x.content)
        #         # await ctx.send_followup(x.content, delete_after=3*60, ephemeral=True)
        #         tosendmsg = tosendmsg + x.content

        if name in x.author.display_name:
            # await ctx.send_followup(x.content, delete_after=3 * 60, ephemeral=True)
            tosendmsg = tosendmsg + "\n" + x.content
            print(f"{x.author.name}: {x.content}")
    if tosendmsg == "":
        tosendmsg = "該当なし"
    await ctx.respond(embed=Embed(description=tosendmsg), delete_after=3 * 60, ephemeral=True)


@bot.slash_command(name="close", description="この部屋に入れる人を限定する。")
async def close(ctx: ApplicationContext):
    global vcRole
    global vcTxt
    global txtMsg
    global guildsettings
    # try:
    #     vcTxt[str(ctx.author.voice.channel.id)]
    # except:
    #     return
    if not str(ctx.author.voice.channel.id) in vcTxt.keys():
        print(traceback.format_exc())
        return
    vc1 = ctx.author.voice.channel
    role1 = ctx.guild.get_role(vcRole[str(ctx.author.voice.channel.id)])
    perm1 = PermissionOverwrite().from_pair(Permissions.advanced().general().voice(), Permissions.none())
    perm2 = PermissionOverwrite().from_pair(Permissions.general(), Permissions.text())
    # perm2.update(connect=True)
    # perm2.update(speak=True)
    # perm2.update(use_slash_commands=True)
    perm2.update(connect=True)
    perm2.update(speak=True)
    # perm1.update(value=689379286592)
    perm1.update(read_message_history=True)
    perm1.update(read_messages=True)
    perm1.update(send_messages=True)
    perm1.update(use_slash_commands=True)
    perm1.update(connect=True, speak=True)
    perms1 = Permissions.advanced().general().voice()
    perm1.update(mute_members=False)
    perm1.update(move_members=False, deafen_members=False)
    perms1.update(mute_members=False, move_members=False, deafen_members=False, connect=True, speak=True)
    # memberRole = message.author.guild.get_role(997644021067415642)
    memberRole = ctx.guild.get_role(guildsettings[str(ctx.guild.id)]["member_role"])
    memberPerm = PermissionOverwrite().from_pair(Permissions.advanced().general(), Permissions.all())
    memberPerm.update(view_channel=True)
    await vc1.edit(overwrites={role1: perm1,
                               memberRole: memberPerm,
                               ctx.guild.default_role: PermissionOverwrite().from_pair(
                                   Permissions.none(),
                                   Permissions.all())
                               }
                   )
    await ctx.respond(embed=Embed(description="完了."))


@bot.slash_command(description="この部屋の名前を変える.")
async def name(ctx: ApplicationContext, name: Option(str, description="名前", required=True)):
    global vcRole
    global vcTxt
    global txtMsg
    global guildsettings
    try:
        txt1 = vcTxt[str(ctx.author.voice.channel.id)]
        txt1 = bot.get_channel(txt1)
    except:
        print(traceback.format_exc())
        return
    await txt1.edit(name=name)
    vc1 = ctx.author.voice.channel
    await vc1.edit(name=name)
    await ctx.respond(embed=Embed(description="完了."))


@bot.slash_command(description="部屋の人数制限を変える")
async def limit(ctx: ApplicationContext, lim: Option(int, description="人数", required=True)):
    global vcRole
    global vcTxt
    global txtMsg
    global guildsettings
    try:
        txt1 = vcTxt[str(ctx.author.voice.channel.id)]
        txt1 = bot.get_channel(txt1)
    except:
        print(traceback.format_exc())
        return
    await ctx.author.voice.channel.edit(user_limit=int(lim))
    await ctx.respond(embed=Embed(description="完了."))


@bot.slash_command(description="この部屋を見えなくする。")
async def nolook(ctx: ApplicationContext):
    global vcRole
    global vcTxt
    global txtMsg
    global guildsettings
    try:
        vcTxt[str(ctx.author.voice.channel.id)]
    except:
        print(traceback.format_exc())
        return
    vc1 = ctx.author.voice.channel
    role1 = ctx.guild.get_role(vcRole[str(ctx.author.voice.channel.id)])
    perm1 = PermissionOverwrite().from_pair(Permissions.advanced().general().voice(), Permissions.none())
    perm2 = PermissionOverwrite().from_pair(Permissions.general(), Permissions.text())
    # perm2.update(connect=True)
    # perm2.update(speak=True)
    # perm2.update(use_slash_commands=True)
    perm2.update(connect=True)
    perm2.update(speak=True)
    # perm1.update(value=689379286592)
    perm1.update(read_message_history=True)
    perm1.update(read_messages=True)
    perm1.update(send_messages=True)
    perm1.update(use_slash_commands=True)
    perm1.update(connect=True, speak=True)
    perms1 = Permissions.advanced().general().voice()
    perm1.update(mute_members=False)
    perm1.update(move_members=False, deafen_members=False)
    perms1.update(mute_members=False, move_members=False, deafen_members=False, connect=True, speak=True)
    # memberRole = message.author.guild.get_role(997644021067415642)
    memberRole = ctx.guild.get_role(guildsettings[str(ctx.guild.id)]["member_role"])
    memberPerm = PermissionOverwrite().from_pair(Permissions.advanced().none(), Permissions.all())
    await vc1.edit(overwrites={
        role1: perm1,
        memberRole: memberPerm,
        ctx.guild.default_role: PermissionOverwrite().from_pair(
            Permissions.none(),
            Permissions.all())}
    )
    await ctx.respond(embed=Embed(description="完了."))

@bot.slash_command(description="この部屋を見えるようにする。")
async def look(ctx: ApplicationContext):
    global vcRole
    global vcTxt
    global txtMsg
    global guildsettings
    try:
        vcTxt[str(ctx.author.voice.channel.id)]
    except:
        print(traceback.format_exc())
        return
    vc1 = ctx.author.voice.channel
    role1 = ctx.guild.get_role(vcRole[str(ctx.author.voice.channel.id)])
    perm1 = PermissionOverwrite().from_pair(Permissions.advanced().general().voice(), Permissions.none())
    perm2 = PermissionOverwrite().from_pair(Permissions.general(), Permissions.text())
    # perm2.update(connect=True)
    # perm2.update(speak=True)
    # perm2.update(use_slash_commands=True)
    perm2.update(connect=True)
    perm2.update(speak=True)
    # perm1.update(value=689379286592)
    perm1.update(read_message_history=True)
    perm1.update(read_messages=True)
    perm1.update(send_messages=True)
    perm1.update(use_slash_commands=True)
    perm1.update(connect=True, speak=True)
    perms1 = Permissions.advanced().general().voice()
    perm1.update(mute_members=False)
    perm1.update(move_members=False, deafen_members=False)
    perms1.update(mute_members=False, move_members=False, deafen_members=False, connect=True, speak=True)
    # perm1 = PermissionOverwrite().from_pair(Permissions.advanced().general().voice(), Permissions.none())
    memberRole = ctx.guild.get_role(guildsettings[str(ctx.guild.id)]["member_role"])
    memberPerm = PermissionOverwrite().from_pair(Permissions.general(), Permissions.text())
    # perm2.update(connect=True)
    # perm2.update(speak=True)
    # perm2.update(use_slash_commands=True)
    memberPerm.update(connect=True)
    memberPerm.update(speak=True)
    # memberRole = message.author.guild.get_role(997644021067415642)
    # memberRole = ctx.guild.get_role(guildsettings[str(ctx.guild.id)]["member_role"])
    # memberPerm = PermissionOverwrite().from_pair(Permissions.advanced().none(), Permissions.all())
    await vc1.edit(overwrites={
        role1: perm1,
        memberRole: memberPerm,
        ctx.guild.default_role: PermissionOverwrite().from_pair(
            Permissions.none(),
            Permissions.all())}
    )
    await ctx.respond(embed=Embed(description="完了."))


@bot.slash_command()
async def ping(ctx: ApplicationContext):
    lat = bot.latency
    await ctx.respond(embed=Embed(description=f"レイテンシーは、{lat * 60}ms."))


@bot.slash_command(guild_ids=[977138017095520256])
async def hello(ctx: ApplicationContext):
    await ctx.respond("Hello!")


@bot.slash_command(description="設定を表示する")
async def set_see(ctx: ApplicationContext):
    global vcRole
    global vcTxt
    global txtMsg
    global guildsettings
    if not ctx.author.guild_permissions.administrator:
        return
    # with open("tmp.json", "w", encoding="utf8")as f:
    #     json.dump(guildsettings[str(ctx.guild.id)], f, ensure_ascii=False)
    # with open("")
    # data = json.loads(str(guildsettings[str(ctx.guild.id)]).replace("'", '"'))
    await ctx.respond(
        embed=Embed(description=json.dumps(guildsettings[str(ctx.guild.id)], indent=2, ensure_ascii=False)))


@bot.slash_command(description="設定を保存して適応する")
async def set_save(ctx: ApplicationContext, json1: Option(str, name="json", required=True, description="設定のjson")):
    global vcRole
    global vcTxt
    global txtMsg
    global guildsettings
    if not ctx.author.guild_permissions.administrator:
        return
    try:
        guildsettings[str(ctx.guild.id)] = json.loads(json1)
        print(json1)
        save_guild_settings()
    except Exception as e:
        await ctx.respond(embed=Embed(description=f"エラー。設定は保存されていません！: {e}"))
        return
    await ctx.respond(embed=Embed(description="設定を保存しました。"))


def save_to_json():
    global vcRole
    global vcTxt
    global txtMsg
    global guildsettings
    print("Saving bot state...")
    with open("vcTxt.json", "w") as f:
        # tmpJson:dict = json.load(f)
        json.dump(vcTxt, f)
    with open("vcRole.json", "w") as f:
        json.dump(vcRole, f)
    with open("txtMsg.json", "w") as f:
        json.dump(txtMsg, f)
    print("Saved bot state.")


def save_guild_settings():
    global vcRole
    global vcTxt
    global txtMsg
    global guildsettings
    print("Saving guildsettings...")
    with open("guildsettings.json", "w", encoding="utf8") as f:
        json.dump(guildsettings, f, ensure_ascii=False)
    print("Saved guildsettings.")


bot.run(TOKEN)
