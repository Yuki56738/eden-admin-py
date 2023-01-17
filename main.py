import os
import traceback

from dotenv import load_dotenv
# pip3 install py-cord[voice] --pre
import discord
from discord import *
from discord.ui import *
from discord.ext import *
import json

import deepl
from google.cloud.firestore_v1 import DocumentReference

import libyuki

from google.cloud import firestore

# from greetings import *

# from discord.ui import *
# import init_db

load_dotenv()
TOKEN = os.environ.get("DISCORD_TOKEN")
DEEPL_KEY = os.environ.get("DEEPL_KEY")

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

# bot.add_cog(Greetings(bot))
# bot.add_cog(init_db.Init_db(bot))
vcRole = {}
vcTxt = {}
txtMsg = {}
guildsettings = {}
vcOwnerRole = {"1234": "2345"}

bot_author_id = 451028171131977738
bot_author = bot.get_user(bot_author_id)
edenNotifyChannel = ""
# bot.load_extension("cogs.init_db")
bot.load_extension("cogs.ticket")
bot.load_extension("cogs.move")


# bot.add_cog()

# class TestView(discord.ui.View):
#     @discord.ui.button(label="Button 1", style=ButtonStyle.red)
#     async def first_button(self, button: discord.ui.Button, interaction: Interaction):
#         await interaction.response(content="ボタンが押されました。", view=self)

class MyModalChangeRoomName(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="部屋の名前", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        # embed = discord.Embed(title="Modal Results")
        # embed.add_field(name="Long Input", value=self.children[0].value)
        # await interaction.response.send_message(embeds=[embed])
        global vcRole
        global vcTxt
        global txtMsg
        global guildsettings
        try:
            # txt1 = vcTxt[str(ctx.author.voice.channel.id)]
            txt1 = vcTxt[str(interaction.user.voice.channel.id)]
            txt1 = bot.get_channel(txt1)
        except:
            print(traceback.format_exc())
            return
        await txt1.edit(name=self.children[0].value)
        # vc1 = ctx.author.voice.channel
        vc1 = interaction.user.voice.channel
        await vc1.edit(name=self.children[0].value)
        await interaction.response.send_message("完了.")
        # await interaction.message.channel.send(embed=Embed(description="完了."))
        # await ctx.respond(embed=Embed(description="完了."))


class MyViewChangeRoomName(discord.ui.View):
    @discord.ui.button(label="部屋の名前を変える.", style=discord.ButtonStyle.blurple)
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(MyModalChangeRoomName(title="部屋の名前を入力..."))

    @discord.ui.button(label="この部屋に入れる人を限定する.", style=discord.ButtonStyle.red)
    async def button2_callback(self, button: Button, interaction: Interaction):
        global vcRole
        global vcTxt
        global txtMsg
        global guildsettings
        # try:
        #     vcTxt[str(ctx.author.voice.channel.id)]
        # except:
        #     return
        if not str(interaction.user.voice.channel.id) in vcTxt.keys():
            print(traceback.format_exc())
            return
        vc1 = interaction.user.voice.channel
        role1 = interaction.guild.get_role(vcRole[str(interaction.user.voice.channel.id)])
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
        memberRole = interaction.guild.get_role(guildsettings[str(interaction.guild.id)]["member_role"])
        memberPerm = PermissionOverwrite().from_pair(Permissions.advanced().general(), Permissions.all())
        memberPerm.update(view_channel=True)
        await vc1.edit(overwrites={role1: perm1,
                                   memberRole: memberPerm,
                                   interaction.guild.default_role: PermissionOverwrite().from_pair(
                                       Permissions.none(),
                                       Permissions.all())
                                   }
                       )

        await interaction.response.send_message(embed=Embed(description="完了."))


class MyModalChangeRoomLimit(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="人数", style=discord.InputTextStyle.singleline))

    async def callback(self, interaction: discord.Interaction):
        # embed = discord.Embed(title="Modal Results")
        # embed.add_field(name="Long Input", value=self.children[0].value)
        # await interaction.response.send_message(embeds=[embed])
        global vcRole
        global vcTxt
        global txtMsg
        global guildsettings
        try:
            txt1 = vcTxt[str(interaction.user.voice.channel.id)]
            txt1 = bot.get_channel(txt1)
        except:
            print(traceback.format_exc())
            return
        await interaction.user.voice.channel.edit(user_limit=int(self.children[0].value))
        await interaction.response.send_message(embed=Embed(description="完了."))


class MyViewChangeRoomLimit(discord.ui.View):
    @discord.ui.button(label="部屋の人数制限を変える", style=discord.ButtonStyle.green)
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(MyModalChangeRoomLimit(title="人数を入力..."))

    @discord.ui.button(label="この部屋を見えなくする", style=discord.ButtonStyle.grey)
    async def button2_callback(self, button, interaction: discord.Interaction):
        # await interaction.response.send_modal(MyModalChangeRoomLimit(title="人数を入力..."))
        global vcRole
        global vcTxt
        global txtMsg
        global guildsettings
        try:
            vcTxt[str(interaction.user.voice.channel.id)]
        except:
            print(traceback.format_exc())
            return
        vc1 = interaction.user.voice.channel
        role1 = interaction.guild.get_role(vcRole[str(interaction.user.voice.channel.id)])
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
        memberRole = interaction.guild.get_role(guildsettings[str(interaction.guild.id)]["member_role"])
        memberPerm = PermissionOverwrite().from_pair(Permissions.advanced().none(), Permissions.all())
        await vc1.edit(overwrites={
            role1: perm1,
            memberRole: memberPerm,
            interaction.guild.default_role: PermissionOverwrite().from_pair(
                Permissions.none(),
                Permissions.all())}
        )
        await interaction.response.send_message("完了.")

    @discord.ui.button(label="この部屋を見えるようにする.", style=ButtonStyle.grey, row=1)
    async def button3_callback(self, button, interaction: Interaction):
        global vcRole
        global vcTxt
        global txtMsg
        global guildsettings
        try:
            vcTxt[str(interaction.user.voice.channel.id)]
        except:
            print(traceback.format_exc())
            return
        vc1 = interaction.user.voice.channel
        role1 = interaction.guild.get_role(vcRole[str(interaction.user.voice.channel.id)])
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
        memberRole = interaction.guild.get_role(guildsettings[str(interaction.guild.id)]["member_role"])
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
            interaction.guild.default_role: PermissionOverwrite().from_pair(
                Permissions.none(),
                Permissions.all())}
        )

        await interaction.response.send_message(embed=Embed(description="完了."))


# @bot.check_once("cogs.move")


@bot.event
async def on_ready():
    global vcRole
    global vcTxt
    global txtMsg
    global guildsettings
    global vcOwnerRole
    print(f"Logged in as: {bot.user}")
    global edenNotifyChannel
    # edenNotifyChannel = bot.get_guild(994483180927201400).get_channel(994483180927201403)
    # await edenNotifyChannel.send(embed=Embed(description="Starting bot..."))
    # await edenNotifyChannel.send(embed=Embed(description="Loading databases..."))
    # bot.get_guild(994483180927201400).fetch_members()
    # bot.activity = "Created by Yuki."
    await bot.change_presence(activity=Game(name="Created by Yuki."))

    # try:
    #     with open("guildsettings.json", "r", encoding="utf8") as f:
    #         guildsettings = json.load(f)
    #     with open("txtMsg.json", "r") as f:
    #         txtMsg = json.load(f)
    #     with open("vcTxt.json", "r") as f:
    #         vcTxt = json.load(f)
    #     with open("vcRole.json", "r") as f:
    #         vcRole = json.load(f)
    #
    #
    # except Exception as e:
    #     print(traceback.format_exc())
    guildsettings = libyuki.get_guilddb_as_dict("guildsettings")
    txtMsg = libyuki.get_guilddb_as_dict("txtMsg")
    vcTxt = libyuki.get_guilddb_as_dict("vcTxt")
    vcRole = libyuki.get_guilddb_as_dict("vcRole")
    vcOwnerRole = libyuki.get_guilddb_as_dict("vcOwnerRole")
    print(guildsettings)
    print("Loaded bot state.")
    # await edenNotifyChannel.send(embed=Embed(description="Loaded databases."))
    db = firestore.Client()
    guildcol = db.collection("guilddb")
    guilddoc = guildcol.document(document_id="guildsettings")
    guilgsettingsDict = guilddoc.get().to_dict()
    txtMsg = guildcol.document(document_id="txtMsg")


@bot.slash_command()
async def reload(ctx: ApplicationContext):
    # bot.remove_cog("Init_db")
    bot.reload_extension("cogs.init_db")
    bot.reload_extension("cogs.ticket")
    bot.reload_extension("cogs.move")
    await ctx.respond("Reload complete.")
    


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
        # print(traceback.format_exc())
        pass
    if isExist == True:
        # bot.get_channel()
        if message.author.id == bot.user.id:

            try:
                msg1_id = txtMsg[str(message.channel.id)]
                msg1 = await message.channel.fetch_message(msg1_id)
                await msg1.delete()
            except Exception as e:
                # print(traceback.format_exc())
                traceback.print_exc()
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
            # print(traceback.format_exc())
            traceback.print_exc()


@bot.event
async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState):
    global vcRole
    global vcTxt
    global txtMsg
    global guildsettings
    global vcOwnerRole
    try:
        guild1 = guildsettings[str(member.guild.id)]
    except:
        # print(traceback.format_exc())
        traceback.format_exc()

    # if not after.channel is None and after.channel.id == 1019948085876629516:
    try:
        if after.channel.id == guildsettings[str(member.guild.id)]["create_vc_channel"]:
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
            ##
            roomOwnerPerm1 = PermissionOverwrite().from_pair(Permissions.advanced().general().voice(),
                                                             Permissions.none())
            roomOwnerPerm1.update(read_message_history=True)
            roomOwnerPerm1.update(read_messages=True)
            roomOwnerPerm1.update(send_messages=True)
            roomOwnerPerm1.update(use_slash_commands=True)
            roomOwnerPerm1.update(connect=True, speak=True)
            roomOwnerPerm1.update(mute_members=False)
            roomOwnerPerm1.update(move_members=False, deafen_members=False, attach_files=True, embed_links=True,
                                  manage_messages=True)
            ##
            perms1.update(mute_members=False, move_members=False, deafen_members=False, connect=True, speak=True)
            # perms1.update(connect=True, speak=True)
            role1 = await member.guild.create_role(name=f"{member.display_name}の部屋", permissions=perms1)
            roomOwnerRole1 = await member.guild.create_role(name=f"{member.display_name}の部屋の主", permissions=perms1)
            await member.add_roles(roomOwnerRole1)
            cat1 = bot.get_channel(guildsettings[str(member.guild.id)]["vc_category"])
            catVc = after.channel.category
            vc1 = await member.guild.create_voice_channel(f"{member.display_name}の部屋",
                                                          overwrites={role1: perm1, memberRole: perm2,
                                                                      roomOwnerRole1: roomOwnerPerm1,
                                                                      member.guild.default_role: PermissionOverwrite().from_pair(
                                                                          Permissions.none(),
                                                                          Permissions.all())},
                                                          category=catVc, user_limit=2)
            vcRole[str(vc1.id)] = role1.id
            # await role1.edit(position=8)
            await member.add_roles(role1)
            await member.move_to(vc1)
            txt1 = await member.guild.create_text_channel(name=f"{member.display_name}の部屋",
                                                          overwrites={role1: perm1, roomOwnerRole1: roomOwnerPerm1,
                                                                      member.guild.default_role: PermissionOverwrite().from_pair(
                                                                          Permissions.none(),
                                                                          Permissions.all())},
                                                          category=catVc)

            vcTxt[str(vc1.id)] = txt1.id
            vcOwnerRole[str(vc1.id)] = roomOwnerRole1.id

            msgToSend = """
Created by Yuki.
/name [名前] で部屋の名前を変える
例｜/name  私のおうち
/limit [人数] で部屋の人数制限を変える
例｜/limit 4（半角
/close でこの部屋に入れる人を限定する。「返信」にてメンションされた人は入れるようになる。
/nolook でこの部屋を見えなくする。
/look で、この部屋を見えるようにする。
            
/menu で、メニューを表示。"""
            # embedToSend = Embed(description=msgToSend)
            msgDescript = await txt1.send(embed=Embed(description=msgToSend))

            await txt1.send(view=MyViewChangeRoomName())
            await txt1.send(view=MyViewChangeRoomLimit())
            # await txt1.send(view=MyViewRoomNolook())

            # ここにボタン等を配置
            # await msgDescript.add_reaction()
            # emoji = '👍'
            # await msgDescript.add_reaction(emoji)
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
                        await txt1.send(embed=Embed(description=msgToSend2))
            except:
                # print(traceback.format_exc())
                traceback.print_exc()
            # msgToSend2 += member.mention
            await txt1.send(member.mention)
            # await txt1.send(embed=Embed(description=msgToSend2))
            save_to_json()
            return
    except:
        pass
    # if not after.channel is None and after.channel.id == guildsettings[str(member.guild.id)]["create_vc_channel_qm_general"]:
    try:
        if after.channel.id == guildsettings[str(member.guild.id)]["create_vc_channel_qm_general"]:
            print("qm_general hit.")
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
            role1 = await member.guild.create_role(name=f"（雑・作）{member.display_name}の部屋", permissions=perms1)
            # cat1 = bot.get_channel(guildsettings[str(member.guild.id)]["vc_category"])
            catVc = after.channel.category
            cat2 = bot.get_channel(guildsettings[str(member.guild.id)]["vc_category"])
            vc1 = await member.guild.create_voice_channel(f"（雑・作）{member.display_name}の部屋",
                                                          overwrites={role1: perm1,
                                                                      memberRole: perm2,
                                                                      member.guild.default_role: PermissionOverwrite().from_pair(
                                                                          Permissions.none(),
                                                                          Permissions.all())
                                                                      },
                                                          category=catVc, user_limit=2)
            vcRole[str(vc1.id)] = role1.id
            # await role1.edit(position=8)
            await member.add_roles(role1)
            await member.move_to(vc1)
            txt1 = await member.guild.create_text_channel(name=f"（雑・作）{member.display_name}の部屋",
                                                          overwrites={role1: perm1,
                                                                      member.guild.default_role: PermissionOverwrite().from_pair(
                                                                          Permissions.none(),
                                                                          Permissions.all())},
                                                          category=cat2)
            vcTxt[str(vc1.id)] = txt1.id
            msgToSend = """
            Created by Yuki.
            /name [名前] で部屋の名前を変える
            例｜/name  私のおうち
            /limit [人数] で部屋の人数制限を変える
            例｜/limit 4（半角
            /close でこの部屋に入れる人を限定する。「返信」にてメンションされた人は入れるようになる。
            /nolook でこの部屋を見えなくする。
            /look で、この部屋を見えるようにする。

            /menu で、メニューを表示。"""
            # embedToSend = Embed(description=msgToSend)
            msgDescript = await txt1.send(embed=Embed(description=msgToSend))

            await txt1.send(view=MyViewChangeRoomName())
            await txt1.send(view=MyViewChangeRoomLimit())
            # await txt1.send(view=MyViewRoomNolook())

            # ここにボタン等を配置
            # await msgDescript.add_reaction()
            # emoji = '👍'
            # await msgDescript.add_reaction(emoji)
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
                        await txt1.send(embed=Embed(description=msgToSend2))
            except:
                # print(traceback.format_exc())
                traceback.print_exc()
            # msgToSend2 += member.mention
            await txt1.send(member.mention)
            # await txt1.send(embed=Embed(description=msgToSend2))
            save_to_json()
    except:
        pass
    try:
        if after.channel.id == guildsettings[str(member.guild.id)]["create_vc_channel_qm_1"]:
            print("qm_1 hit.")
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
            role1 = await member.guild.create_role(name=f"（猥・エ）{member.display_name}の部屋", permissions=perms1)
            # cat1 = bot.get_channel(guildsettings[str(member.guild.id)]["vc_category"])
            # cat2 = after.channel.category
            cat2 = bot.get_channel(guildsettings[str(member.guild.id)]["vc_category"])
            catVc = after.channel.category
            vc1 = await member.guild.create_voice_channel(f"（猥・エ）{member.display_name}の部屋", overwrites={role1: perm1,
                                                                                                           memberRole: perm2,
                                                                                                           member.guild.default_role: PermissionOverwrite().from_pair(
                                                                                                               Permissions.none(),
                                                                                                               Permissions.all())
                                                                                                           },
                                                          category=catVc, user_limit=2)
            vcRole[str(vc1.id)] = role1.id
            # await role1.edit(position=8)
            await member.add_roles(role1)
            await member.move_to(vc1)
            txt1 = await member.guild.create_text_channel(name=f"（猥・エ）{member.display_name}の部屋",
                                                          overwrites={role1: perm1,
                                                                      member.guild.default_role: PermissionOverwrite().from_pair(
                                                                          Permissions.none(),
                                                                          Permissions.all())},
                                                          category=cat2)
            vcTxt[str(vc1.id)] = txt1.id
            msgToSend = """
Created by Yuki.
/name [名前] で部屋の名前を変える
例｜/name 私のおうち
/limit [人数] で部屋の人数制限を変える
例｜/limit 4（半角
/close でこの部屋に入れる人を限定する。「返信」にてメンションされた人は入れるようになる。
/nolook でこの部屋を見えなくする。
/look で、この部屋を見えるようにする。
 
/menu で、メニューを表示。"""
            # embedToSend = Embed(description=msgToSend)
            msgDescript = await txt1.send(embed=Embed(description=msgToSend))

            await txt1.send(view=MyViewChangeRoomName())
            await txt1.send(view=MyViewChangeRoomLimit())
            # await txt1.send(view=MyViewRoomNolook())

            # ここにボタン等を配置
            # await msgDescript.add_reaction()
            # emoji = '👍'
            # await msgDescript.add_reaction(emoji)
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
                        await txt1.send(embed=Embed(description=msgToSend2))
            except:
                # print(traceback.format_exc())
                traceback.print_exc()
            # msgToSend2 += member.mention
            await txt1.send(member.mention)
            # await txt1.send(embed=Embed(description=msgToSend2))
            save_to_json()
    except:
        pass
    try:
        if after.channel.id == guildsettings[str(member.guild.id)]["create_vc_channel_qm_2"]:
            print("qm_2 hit.")
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
            role1 = await member.guild.create_role(name=f"（寝）{member.display_name}の部屋", permissions=perms1)
            # cat1 = bot.get_channel(guildsettings[str(member.guild.id)]["vc_category"])
            # cat2 = after.channel.category
            cat2 = bot.get_channel(guildsettings[str(member.guild.id)]["vc_category"])
            catVc = after.channel.category
            vc1 = await member.guild.create_voice_channel(f"（寝）{member.display_name}の部屋", overwrites={role1: perm1,
                                                                                                         memberRole: perm2,
                                                                                                         member.guild.default_role: PermissionOverwrite().from_pair(
                                                                                                             Permissions.none(),
                                                                                                             Permissions.all())
                                                                                                         },
                                                          category=catVc, user_limit=2)
            vcRole[str(vc1.id)] = role1.id
            # await role1.edit(position=8)
            await member.add_roles(role1)
            await member.move_to(vc1)
            txt1 = await member.guild.create_text_channel(name=f"（寝）{member.display_name}の部屋",
                                                          overwrites={role1: perm1,
                                                                      member.guild.default_role: PermissionOverwrite().from_pair(
                                                                          Permissions.none(),
                                                                          Permissions.all())},
                                                          category=cat2)
            vcTxt[str(vc1.id)] = txt1.id
            msgToSend = """
            Created by Yuki.
            /name [名前] で部屋の名前を変える
            例｜/name  私のおうち
            /limit [人数] で部屋の人数制限を変える
            例｜/limit 4（半角
            /close でこの部屋に入れる人を限定する。「返信」にてメンションされた人は入れるようになる。
            /nolook でこの部屋を見えなくする。
            /look で、この部屋を見えるようにする。

            /menu で、メニューを表示。"""
            # embedToSend = Embed(description=msgToSend)
            msgDescript = await txt1.send(embed=Embed(description=msgToSend))

            await txt1.send(view=MyViewChangeRoomName())
            await txt1.send(view=MyViewChangeRoomLimit())
            # await txt1.send(view=MyViewRoomNolook())

            # ここにボタン等を配置
            # await msgDescript.add_reaction()
            # emoji = '👍'
            # await msgDescript.add_reaction(emoji)
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
                        await txt1.send(embed=Embed(description=msgToSend2))
            except:
                # print(traceback.format_exc())
                traceback.print_exc()
            # msgToSend2 += member.mention
            await txt1.send(member.mention)
            # await txt1.send(embed=Embed(description=msgToSend2))
            save_to_json()
    except:
        pass

    if not before.channel is None:
        txt1_id = vcTxt[str(before.channel.id)]
        txt1 = bot.get_channel(txt1_id)
        role1 = vcRole[str(before.channel.id)]
        role1 = member.guild.get_role(role1)
        if len(before.channel.members) == 0:
            await txt1.delete()
            await role1.delete()
            await before.channel.delete()
            vcRole.pop(str(before.channel.id))
            vcTxt.pop(str(before.channel.id))
            save_to_json()
            try:
                await member.guild.get_role(vcOwnerRole[str(before.channel.id)]).delete()
                vcOwnerRole.pop(str(before.channel.id))
            except:
                pass
            await member.remove_roles(role1)

    # if before.channel.id is None and after.channel.id is None:
    #     return
    if before.channel != after.channel:
        try:
            role1 = vcRole[str(after.channel.id)]
            role1 = member.guild.get_role(role1)
            txt1 = vcTxt[str(after.channel.id)]

            txt1: TextChannel = bot.get_channel(txt1)
            await member.add_roles(role1)
            save_to_json()
            # prof_channel = bot.get_channel(995656569301774456)
            prof_channel_id = guildsettings[str(member.guild.id)]["prof_channel"]
            prof_channel = bot.get_channel(prof_channel_id)
            prof_messages = await prof_channel.history(limit=1000).flatten()
            for x in prof_messages:
                if x.author.id == member.id:
                    msgToSend = ""
                    msgToSend += x.content
                    # await txt1.send(embed=embedToSend)
                    await txt1.send(embed=Embed(description=msgToSend))
            await txt1.send(member.mention)
            await txt1.send(view=MyViewChangeRoomName())
            await txt1.send(view=MyViewChangeRoomLimit())
            save_to_json()
        except:
            traceback.format_exc()

            # if not before.channel is None and len(before.channel.members) == 0:

            save_to_json()
    if after.channel is None:
        return


class MyViewTicket(discord.ui.View):
    @discord.ui.button(label="問題を作成", style=discord.ButtonStyle.green)
    async def button_callback(self, button, interaction: Interaction):
        # await interaction.response.send("頑張っています...")
        await interaction.response.send_message("頑張っています...")
        # await interaction.response.send_modal(MyModalChangeRoomLimit(title="人数を入力..."))
        permow1 = PermissionOverwrite().from_pair(Permissions.text(), Permissions.none())
        permow2 = PermissionOverwrite().from_pair(Permissions.none(), Permissions.all())
        # memberRole = ctx.guild.get_role(guildsettings[str(member.guild.id)]["member_role"])
        db = firestore.Client()
        guilddb = db.collection("guilddb")
        guilddb1 = guilddb.document(document_id="guildsettings")
        guilddb1_dict = guilddb1.get().to_dict()
        cat1 = guilddb1_dict[str(interaction.guild.id)]["ticket_category"]
        cat1 = bot.get_channel(cat1)
        # cat1 = guilddb1_dict[str(interaction.guild.id)]["ticket_category"]
        # cat1 = bot.get_channel(cat1)
        # cat1 = interaction.channel

        txt1: TextChannel = await interaction.guild.create_text_channel(name=f"{interaction.user.display_name}のticket",
                                                                        category=cat1,
                                                                        overwrites={
                                                                            interaction.guild.default_role: permow2,
                                                                            interaction.user: permow1
                                                                        })
        db = firestore.Client()
        db1 = db.collection("guilddb").document(document_id="ticketTxtUser")
        db1_dict = db1.get().to_dict()
        if db1_dict is None:
            db1_dict1 = {
                str(txt1.id): str(interaction.user.id)
            }
            db1.create(db1_dict1)

        db1_dict[str(txt1.id)] = str(interaction.user.id)
        print(db1.update(db1_dict))
        # db1.update(db1_dict)
        await txt1.send(f"問題が作成されました。ただいま対応しますので、少々お待ちください... {interaction.user.mention}")


# @bot.slash_command(description="問題を報告する")
# async def ticket(ctx: ApplicationContext):
#     if not ctx.user.guild_permissions.administrator:
#         await ctx.respond("現在このコマンドは管理者のみ使用できます。")
#         return
#     await ctx.respond("頑張っています...")
#
#     # cat1 = ctx.guild.get_channel(guildsettings[ctx.guild.id]["ticket_category"])
#     # ticket_channel = ctx.guild.get_channel(libyuki.get_guilddb_as_dict("guildsettings")["994483180927201400"]["ticket_channel"])
#     # await ctx.respond(view=MyViewTicket())
#     # await ticket_channel.send(view=MyViewTicket())
#     return
#
#     permow1 = PermissionOverwrite().from_pair(Permissions.text(), Permissions.none())
#     permow2 = PermissionOverwrite().from_pair(Permissions.none(), Permissions.all())
#     # memberRole = ctx.guild.get_role(guildsettings[str(member.guild.id)]["member_role"])
#     cat1 = libyuki.get_guilddb_as_dict("guildsettings")[ctx.guild.id]["ticket_category"]
#     txt1: TextChannel = await ctx.guild.create_text_channel(name=f"{ctx.user.display_name}のticket", category=cat1,
#                                                             overwrites={
#                                                                 ctx.guild.default_role: permow2,
#                                                                 ctx.user: permow1
#                                                             })
#     db = firestore.Client()
#     db1 = db.collection("guilddb").document(document_id="ticketTxtUser")
#     db1_dict = db1.get().to_dict()
#     db1_dict[str(ctx.user.id)] = str(txt1.id)
#     db1.update(db1_dict)
#     await txt1.send(f"問題が作成されました。ただいま対応しますので、少々お待ちください... {ctx.user.mention}")


@bot.slash_command(description="メニューを表示")
async def menu(ctx: ApplicationContext):
    global vcRole
    global vcTxt
    global txtMsg
    global guildsettings
    # isCreatedRoom = True
    isGeneral = False
    try:
        txt1 = vcTxt[str(ctx.author.voice.channel.id)]
        txt1 = bot.get_channel(txt1)
    except:
        # print(traceback.format_exc())
        traceback.print_exc()
        isGeneral = True
    # if isGeneral:
    #     await ctx.respond(view=MyViewMoveMember(), delete_after=3 * 60)

    else:
        await ctx.respond(view=MyViewChangeRoomName(), ephemeral=True)
        await ctx.send_followup(view=MyViewChangeRoomLimit(), ephemeral=True)
    # await ctx.send(view=MyViewRoomNolook())
    # await txt1.send(view=MyViewChangeRoomName())
    # await txt1.send(view=MyViewChangeRoomLimit())


@bot.slash_command(description="自己紹介を表示")
async def prof(ctx: ApplicationContext, name: Option(str, required=True, description="名前")):
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
            tosendmsg = tosendmsg + x.content
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


def save_to_json():
    global vcRole
    global vcTxt
    global txtMsg
    global guildsettings
    global vcOwnerRole
    print("Saving bot state...")
    # with open("vcTxt.json", "w") as f:
    #     # tmpJson:dict = json.load(f)
    #     json.dump(vcTxt, f)
    # with open("vcRole.json", "w") as f:
    #     json.dump(vcRole, f)
    # with open("txtMsg.json", "w") as f:
    #     json.dump(txtMsg, f)
    # global edenNotifyChannel
    libyuki.push_guilddb(id="vcTxt", payload=vcTxt)
    libyuki.push_guilddb(id="vcRole", payload=vcRole)
    libyuki.push_guilddb(id="txtMsg", payload=txtMsg)
    libyuki.push_guilddb(id="vcOwnerRole", payload=vcOwnerRole)
    print("Saved bot state.")


def save_guild_settings():
    global vcRole
    global vcTxt
    global txtMsg
    global guildsettings
    print("Saving guildsettings...")
    # with open("guildsettings.json", "w", encoding="utf8") as f:
    #     json.dump(guildsettings, f, ensure_ascii=False)
    libyuki.push_guilddb(id="guildsettings", payload=guildsettings)
    print("Saved guildsettings.")


bot.run(TOKEN)
