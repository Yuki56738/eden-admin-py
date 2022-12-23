import os
import traceback

from dotenv import load_dotenv
import discord
from discord import *
import json

import deepl

# from discord.ui import *

load_dotenv(".envDev")
TOKEN = os.environ.get("DISCORD_TOKEN")
DEEPL_KEY = os.environ.get("DEEPL_KEY")


intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

vcRole = {}
vcTxt = {}
txtMsg = {}
guildsettings = {}


bot_author_id = 451028171131977738
bot_author = bot.get_user(bot_author_id)

# class TestView(discord.ui.View):
#     @discord.ui.button(label="Button 1", style=ButtonStyle.red)
#     async def first_button(self, button: discord.ui.Button, interaction: Interaction):
#         await interaction.response(content="ボタンが押されました。", view=self)

class MyView(discord.ui.View):
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Choose a Flavor!", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maximum number of values that can be selected by the users
        options = [ # the list of options from which users can choose, a required field
            discord.SelectOption(
                label="Vanilla",
                description="Pick this if you like vanilla!"
            ),
            discord.SelectOption(
                label="Chocolate",
                description="Pick this if you like chocolate!"
            ),
            discord.SelectOption(
                label="Strawberry",
                description="Pick this if you like strawberry!"
            )
        ]
    )
    async def select_callback(self, select, interaction): # the function called when the user is done selecting options
        await interaction.response.send_message(f"Awesome! I like {select.values[0]} too!")


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
    # if message.content.startswith("y.help"):
    #     msgToSend = Embed(title="Yukiの管理BOT", description="y.show または my.show -> 自分の自己紹介を表示する。")
    #     await message.channel.send(embed=msgToSend, delete_after=3 * 60)
    if message.content.startswith(".debug"):
        print(f"vcRole: {vcRole}")
        print(f"vcTxt: {vcTxt}")

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
        # embedToSend = Embed(description=msgToSend)
        msgDescript = await txt1.send(embed=Embed(description=msgToSend))


        #ここにボタン等を配置
        # await msgDescript.add_reaction()
        emoji = '👍'
        await msgDescript.add_reaction(emoji)

        await txt1.send("Choose a flavor!", view=MyView())

        msgToSend2 = ""
        try:
            # prof_channel = bot.get_channel(995656569301774456)
            prof_channel_id = guildsettings[str(member.guild.id)]["prof_channel"]
            prof_channel = bot.get_channel(prof_channel_id)
            prof_messages = await prof_channel.history(limit=1000).flatten()
            for x in prof_messages:
                if x.author.id == member.id:
                    # await txt1.send(x.content)
                    # await txt1.send(embed=Embed(description=x.content))
                    msgToSend2 += x.content
        except:
            print(traceback.format_exc())
        # msgToSend2 += member.mention
        await txt1.send(member.mention)
        await txt1.send(embed=Embed(description=msgToSend2))
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
                    embedToSend = Embed
                    await txt1.send(embed=embedToSend)
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

@bot.slash_command(description="Do translation.")
async def trans(ctx: ApplicationContext, *, text):
    translator = deepl.Translator(DEEPL_KEY)
    result = translator.translate_text(text, target_lang='JA')
    await ctx.respond(text)
    await ctx.send(result)

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
