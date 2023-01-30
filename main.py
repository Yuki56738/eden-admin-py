import os
import traceback

from dotenv import load_dotenv
# pip3 install py-cord[voice] --pre
import discord
from discord import *
from discord.ui import *
from discord.ext import *
# import json

# import deepl
# from google.cloud.firestore_v1 import DocumentReference

# import libyuki

from google.cloud import firestore

# import cogs.menu

# from greetings import *

# from discord.ui import *
# import init_db

load_dotenv()
TOKEN = os.environ.get("DISCORD_TOKEN")
# DEEPL_KEY = os.environ.get("DEEPL_KEY")

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)
db = firestore.Client()

# bot.add_cog(Greetings(bot))
# bot.add_cog(init_db.Init_db(bot))
# vcRole = {}
# vcTxt = {}
# txtMsg = {}
# guildsettings = {}
# vcOwnerRole = {"1234": "2345"}

bot_author_id = 451028171131977738
bot_author = bot.get_user(bot_author_id)
edenNotifyChannel = ""
# bot.load_extension("cogs.init_db")
# bot.load_extension("cogs.ticket")
bot.load_extension("cogs.move")
bot.load_extension('cogs.note')
bot.load_extension('cogs.menu')
# bot.load_extension('cogs.ticket2')


# bot.load_extension('cogs.init_db')
# bot.load_extension('cogs.init_db')


# guildsettings = guilddb.document(str(member.guild.id))
# db = Client()


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
        # global vcRole
        # global vcTxt
        # global txtMsg
        # global guildsettings
        # db = firestore.Client()
        global db
        # guilddbRef = db.collection(str(interaction.guild.id)).document('settings')
        vcRoleRef = db.collection(str(interaction.guild.id)).document('vcRole')
        if not str(interaction.channel_id) in vcRoleRef.get().to_dict().keys():
            return
        # try:
        #     # txt1 = vcTxt[str(ctx.author.voice.channel.id)]
        #     # txt1 = vcTxt[str(interaction.user.voice.channel.id)]
        #     # txt1_id = vcRoleRef.get().to_dict()[str(interaction.user.voice.channel.id)]
        #     # txt1 = bot.get_channel(txt1_id)
        # except:
        #     print(traceback.format_exc())
        #     return
        await interaction.user.voice.channel.edit(name=self.children[0].value)
        # await txt1.edit(name=self.children[0].value)
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

    @discord.ui.button(label="部屋の人数制限を変える", style=discord.ButtonStyle.green)
    async def button2_callback(self, button, interaction):
        await interaction.response.send_modal(MyModalChangeRoomLimit(title="人数を入力..."))

    @discord.ui.button(label="この部屋を見えなくする", style=discord.ButtonStyle.grey)
    async def button3_callback(self, button, interaction: discord.Interaction):
        # await interaction.response.send_modal(MyModalChangeRoomLimit(title="人数を入力..."))
        # global vcRole
        # global vcTxt
        # global txtMsg
        # global guildsettings
        # db = firestore.Client()
        global db
        guilddbRef = db.collection(str(interaction.guild.id)).document('settings')
        vcRoleRef = db.collection(str(interaction.guild.id)).document('vcRole')
        # try:
        # vcTxt[str(interaction.user.voice.channel.id)]
        if vcRoleRef.get().to_dict().get(str(interaction.user.voice.channel.id)) is None:
            return
        # except:
        #     print(traceback.format_exc())
        #     return
        vc1 = interaction.user.voice.channel
        # role1 = interaction.guild.get_role(vcRole[str(interaction.user.voice.channel.id)])
        role1_id = vcRoleRef.get().to_dict()[str(vc1.id)]
        role1 = interaction.guild.get_role(int(role1_id))
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
        # memberRole = interaction.guild.get_role(guildsettings[str(interaction.guild.id)]["member_role"])
        memberRole_id = guilddbRef.get().to_dict()['member_role']
        memberRole = interaction.guild.get_role(int(memberRole_id))
        memberPerm = PermissionOverwrite().from_pair(Permissions.advanced().none(), Permissions.all())
        await vc1.edit(overwrites={
            role1: perm1,
            memberRole: memberPerm,
            interaction.guild.default_role: PermissionOverwrite().from_pair(
                Permissions.none(),
                Permissions.all())}
        )
        await interaction.response.send_message("完了.")


class MyModalChangeRoomLimit(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="人数", style=discord.InputTextStyle.singleline))

    async def callback(self, interaction: discord.Interaction):
        # embed = discord.Embed(title="Modal Results")
        # embed.add_field(name="Long Input", value=self.children[0].value)
        # await interaction.response.send_message(embeds=[embed])
        # global vcRole
        # global vcTxt
        # global txtMsg
        # global guildsettings
        global db
        vcRoleRef = db.collection(str(interaction.guild.id)).document('vcRole')
        if not str(interaction.channel_id) in vcRoleRef.get().to_dict().keys():
            return
        # guilddbRef = db.collection(str(interaction.channel.id)).document('settings')
        # print(guilddbRef.get().to_dict())
        # if interaction
        # try:
        # txt1 = vcTxt[str(interaction.user.voice.channel.id)]

        # txt1 = bot.get_channel(txt1)

        # except:
        #     print(traceback.format_exc())
        #     return

        await interaction.user.voice.channel.edit(user_limit=int(self.children[0].value))
        await interaction.response.send_message(embed=Embed(description="完了."))

#
# class MyViewChangeRoomLimit(discord.ui.View):
#     @discord.ui.button(label="部屋の人数制限を変える", style=discord.ButtonStyle.green)
#     async def button_callback(self, button, interaction):
#         await interaction.response.send_modal(MyModalChangeRoomLimit(title="人数を入力..."))
#
#     @discord.ui.button(label="この部屋を見えなくする", style=discord.ButtonStyle.grey)
#     async def button2_callback(self, button, interaction: discord.Interaction):
#         # await interaction.response.send_modal(MyModalChangeRoomLimit(title="人数を入力..."))
#         # global vcRole
#         # global vcTxt
#         # global txtMsg
#         # global guildsettings
#         # db = firestore.Client()
#         global db
#         guilddbRef = db.collection(str(interaction.guild.id)).document('settings')
#         vcRoleRef = db.collection(str(interaction.guild.id)).document('vcRole')
#         # try:
#         # vcTxt[str(interaction.user.voice.channel.id)]
#         if vcRoleRef.get().to_dict().get(str(interaction.user.voice.channel.id)) is None:
#             return
#         # except:
#         #     print(traceback.format_exc())
#         #     return
#         vc1 = interaction.user.voice.channel
#         role1 = interaction.guild.get_role(vcRole[str(interaction.user.voice.channel.id)])
#         perm1 = PermissionOverwrite().from_pair(Permissions.advanced().general().voice(), Permissions.none())
#         perm2 = PermissionOverwrite().from_pair(Permissions.general(), Permissions.text())
#         # perm2.update(connect=True)
#         # perm2.update(speak=True)
#         # perm2.update(use_slash_commands=True)
#         perm2.update(connect=True)
#         perm2.update(speak=True)
#         # perm1.update(value=689379286592)
#         perm1.update(read_message_history=True)
#         perm1.update(read_messages=True)
#         perm1.update(send_messages=True)
#         perm1.update(use_slash_commands=True)
#         perm1.update(connect=True, speak=True)
#         perms1 = Permissions.advanced().general().voice()
#         perm1.update(mute_members=False)
#         perm1.update(move_members=False, deafen_members=False)
#         perms1.update(mute_members=False, move_members=False, deafen_members=False, connect=True, speak=True)
#         # memberRole = message.author.guild.get_role(997644021067415642)
#         memberRole = interaction.guild.get_role(guildsettings[str(interaction.guild.id)]["member_role"])
#         memberPerm = PermissionOverwrite().from_pair(Permissions.advanced().none(), Permissions.all())
#         await vc1.edit(overwrites={
#             role1: perm1,
#             memberRole: memberPerm,
#             interaction.guild.default_role: PermissionOverwrite().from_pair(
#                 Permissions.none(),
#                 Permissions.all())}
#         )
#         await interaction.response.send_message("完了.")
#
#     @discord.ui.button(label="この部屋を見えるようにする.", style=ButtonStyle.grey, row=1)
#     async def button3_callback(self, button, interaction: Interaction):
#         # global vcRole
#         # global vcTxt
#         # global txtMsg
#         # global guildsettings
#         # db = firestore.Client()
#         global db
#         guilddbRef = db.collection(str(interaction.guild.id)).document('settings')
#         vcRoleRef = db.collection(str(interaction.guild.id)).document('vcRole')
#
#         vc1 = interaction.user.voice.channel
#         role1_id = vcRoleRef.get().to_dict()[str(interaction.user.voice.channel.id)]
#         role1 = interaction.guild.get_role(int(role1_id))
#         perm1 = PermissionOverwrite().from_pair(Permissions.advanced().general().voice(), Permissions.none())
#         perm2 = PermissionOverwrite().from_pair(Permissions.general(), Permissions.text())
#         # perm2.update(connect=True)
#         # perm2.update(speak=True)
#         # perm2.update(use_slash_commands=True)
#         perm2.update(connect=True)
#         perm2.update(speak=True)
#         # perm1.update(value=689379286592)
#         perm1.update(read_message_history=True)
#         perm1.update(read_messages=True)
#         perm1.update(send_messages=True)
#         perm1.update(use_slash_commands=True)
#         perm1.update(connect=True, speak=True)
#         perms1 = Permissions.advanced().general().voice()
#         perm1.update(mute_members=False)
#         perm1.update(move_members=False, deafen_members=False)
#         perms1.update(mute_members=False, move_members=False, deafen_members=False, connect=True, speak=True)
#         # perm1 = PermissionOverwrite().from_pair(Permissions.advanced().general().voice(), Permissions.none())
#         # memberRole = interaction.guild.get_role(guildsettings[str(interaction.guild.id)]["member_role"])
#         memberRole_id = guilddbRef.get().to_dict()['member_role']
#         memberRole = interaction.guild.get_role(memberRole_id)
#         memberPerm = PermissionOverwrite().from_pair(Permissions.general(), Permissions.text())
#         # perm2.update(connect=True)
#         # perm2.update(speak=True)
#         # perm2.update(use_slash_commands=True)
#         memberPerm.update(connect=True)
#         memberPerm.update(speak=True)
#         # memberRole = message.author.guild.get_role(997644021067415642)
#         # memberRole = ctx.guild.get_role(guildsettings[str(ctx.guild.id)]["member_role"])
#         # memberPerm = PermissionOverwrite().from_pair(Permissions.advanced().none(), Permissions.all())
#         await vc1.edit(overwrites={
#             role1: perm1,
#             memberRole: memberPerm,
#             interaction.guild.default_role: PermissionOverwrite().from_pair(
#                 Permissions.none(),
#                 Permissions.all())}
#         )
#
#         await interaction.response.send_message(embed=Embed(description="完了."))


# @bot.check_once("cogs.move")

# def init():

@bot.event
async def on_ready():
    # global vcRole
    # global vcTxt
    # global txtMsg
    # global guildsettings
    # global vcOwnerRole
    print(f"Logged in as: {bot.user}")
    # global edenNotifyChannel
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
    # guildsettings = libyuki.get_guilddb_as_dict('guildsettings')
    # txtMsg = libyuki.get_guilddb_as_dict("txtMsg")
    # vcTxt = libyuki.get_guilddb_as_dict("vcTxt")
    # vcRole = libyuki.get_guilddb_as_dict("vcRole")
    # vcOwnerRole = libyuki.get_guilddb_as_dict("vcOwnerRole")
    # print(guildsettings)
    # print("Loaded bot state.")
    # await edenNotifyChannel.send(embed=Embed(description="Loaded databases."))
    # db = firestore.Client()
    # guildcol = db.collection("guilddb")
    # guilddoc = guildcol.document(document_id="guildsettings")
    # guilgsettingsDict = guilddoc.get().to_dict()
    # txtMsg = guildcol.document(document_id="txtMsg")
    # txtMsg = libyuki.get_guilddb_as_dict("txtMsg")


# @bot.slash_command()
# async def reload(ctx: ApplicationContext):
# bot.reload_extension("cogs.init_db")
# bot.reload_extension("cogs.ticket")
# bot.reload_extension("cogs.move")
# bot.reload_extension('cogs.init_db')
# await ctx.respond("Reload complete.")


@bot.event
async def on_raw_reaction_add(reaction: RawReactionActionEvent):
    # global vcRole
    # global vcTxt
    # global txtMsg
    # global guildsettings
    print("reaction")
    # reaction_channel_id = guildsettings[str(reaction.guild_id)]["reaction_channel"]
    # db = firestore.Client()
    global db
    guilddbRef = db.collection(str(reaction.guild_id)).document('settings')
    listen_channel_id = guilddbRef.get().to_dict()['listen_channel']
    notify_channel_id = guilddbRef.get().to_dict()['notify_channel']
    notify_channel = bot.get_channel(int(notify_channel_id))
    listen_channel = bot.get_channel(int(listen_channel_id))
    msg1 = await listen_channel.fetch_message(reaction.message_id)
    if reaction.channel_id == listen_channel.id:
        await notify_channel.send(f"{reaction.member.mention} から {msg1.author.mention} へ反応がありました！")


# @bot.event
# async def on_message(message: Message):
#     global vcRole
#     global vcTxt
#     global txtMsg
#     global guildsettings
#     if message.author.bot:
#         return
#     # if message.content.startswith("y.help"):
#     #     msgToSend = Embed(title="Yukiの管理BOT", description="y.show または my.show -> 自分の自己紹介を表示する。")
#     #     await message.channel.send(embed=msgToSend, delete_after=3 * 60)
#     if message.content.startswith(".debug"):
#         print(f"vcRole: {vcRole}")
#         print(f"vcTxt: {vcTxt}")
#     guildsettings = libyuki.get_guilddb_as_dict("guildsettings")
#     isExist = False
#     try:
#         guildsettings[str(message.guild.id)]["note_channels"][str(message.channel.id)]
#         isExist = True
#     except Exception as e:
#         # print(traceback.format_exc())
#         traceback.print_exc()
#     if isExist == True:
#         try:
#             msg1_id = txtMsg[str(message.channel.id)]
#             msg1 = await message.channel.fetch_message(msg1_id)
#             await msg1.delete()
#         except Exception as e:
#             # print(traceback.format_exc())
#             traceback.print_exc()
#         tosendtxt = guildsettings[str(message.guild.id)]["note_channels"][str(message.channel.id)]
#         msg2 = await message.channel.send(embed=Embed(description=tosendtxt))
#         txtMsg[str(message.channel.id)] = msg2.id
#         save_to_json()
#
#     if message.mentions:
#         try:
#             vc1 = message.author.voice.channel
#             txt1_id = vcTxt[str(str(vc1.id))]
#             txt1 = bot.get_channel(txt1_id)
#             perm1 = PermissionOverwrite().from_pair(Permissions.advanced().general().voice(), Permissions.none())
#             perm2 = PermissionOverwrite().from_pair(Permissions.general(), Permissions.text())
#             # perm2.update(connect=True)
#             # perm2.update(speak=True)
#             # perm2.update(use_slash_commands=True)
#             perm2.update(connect=True)
#             perm2.update(speak=True)
#             # perm1.update(value=689379286592)
#             perm1.update(read_message_history=True)
#             perm1.update(read_messages=True)
#             perm1.update(send_messages=True)
#             perm1.update(use_slash_commands=True)
#             perm1.update(connect=True, speak=True)
#             perms1 = Permissions.advanced().general().voice()
#             perm1.update(mute_members=False)
#             perm1.update(move_members=False, deafen_members=False)
#             role1 = message.guild.get_role(vcRole[str(vc1.id)])
#             if message.channel.id == guildsettings[str(message.guild.id)]["mention_channel"]:
#                 for x in message.mentions:
#                     await x.add_roles(role1)
#                     await vc1.edit(overwrites={x: perm1})
#         except:
#             # print(traceback.format_exc())
#             traceback.print_exc()


@bot.event
async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState):
    global db
    guilddbRef = db.collection(str(member.guild.id)).document('settings')
    vcRoleRef = db.collection(str(member.guild.id)).document('vcRole')
    print('guilddbRef.get().to_dict():', guilddbRef.get().to_dict())
    print('create_vc_channel:', guilddbRef.get().to_dict()['create_vc_channel'])
    try:
        if str(after.channel.id) == str(guilddbRef.get().to_dict()['create_vc_channel']):
            print("hit. create_vc_channel.")
            memberRole_id = guilddbRef.get().to_dict()['member_role']
            print(memberRole_id)
            memberRole = member.guild.get_role(int(memberRole_id))
            perm1 = PermissionOverwrite().from_pair(Permissions.advanced().general().voice(), Permissions.none())
            perm2 = PermissionOverwrite().from_pair(Permissions.general(), Permissions.text())
            perm2.update(connect=True)
            perm2.update(speak=True)
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
            # roomOwnerRole1 = await member.guild.create_role(name=f"{member.display_name}の部屋の主", permissions=perms1)
            # await member.add_roles(roomOwnerRole1)
            # cat1 = bot.get_channel(guildsettings[str(member.guild.id)]["vc_category"])
            catVc = after.channel.category
            vc1 = await member.guild.create_voice_channel(f"{member.display_name}の部屋",
                                                          overwrites={role1: perm1, memberRole: perm2,
                                                                      # roomOwnerRole1: roomOwnerPerm1,
                                                                      member.guild.default_role: PermissionOverwrite().from_pair(
                                                                          Permissions.none(),
                                                                          Permissions.all())},
                                                          category=catVc, user_limit=2)
            # vcRole[str(vc1.id)] = role1.id
            # await role1.edit(position=8)
            #
            vcRoleRef.update({
                str(vc1.id): role1.id
            })
            await member.add_roles(role1)
            await member.move_to(vc1)

        if str(after.channel.id) == str(guilddbRef.get().to_dict()['create_qm_general']):
            print("hit. qm_general")
            # await member.guild.system_channel.send("hit.")
            # memberRole = member.guild.get_role(997644021067415642)
            # memberRole = member.guild.get_role(guildsettings.get().to_dict()[str(member.guild.id)]["member_role"])
            memberRole_id = guilddbRef.get().to_dict()['member_role']
            print(memberRole_id)
            memberRole = member.guild.get_role(int(memberRole_id))
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
            # roomOwnerRole1 = await member.guild.create_role(name=f"{member.display_name}の部屋の主", permissions=perms1)
            # await member.add_roles(roomOwnerRole1)
            # cat1 = bot.get_channel(guildsettings[str(member.guild.id)]["vc_category"])
            catVc = after.channel.category
            vc1 = await member.guild.create_voice_channel(f"（雑・作）{member.display_name}の部屋",
                                                          overwrites={role1: perm1, memberRole: perm2,
                                                                      # roomOwnerRole1: roomOwnerPerm1,
                                                                      member.guild.default_role: PermissionOverwrite().from_pair(
                                                                          Permissions.none(),
                                                                          Permissions.all())},
                                                          category=catVc, user_limit=2)
            # vcRole[str(vc1.id)] = role1.id
            # await role1.edit(position=8)
            #
            vcRoleRef.update({
                str(vc1.id): role1.id
            })
            await member.add_roles(role1)
            await member.move_to(vc1)
            # return

        if str(after.channel.id) == str(guilddbRef.get().to_dict()['create_qm_1']):
            print("hit. qm 1")
            # await member.guild.system_channel.send("hit.")
            # memberRole = member.guild.get_role(997644021067415642)
            # memberRole = member.guild.get_role(guildsettings.get().to_dict()[str(member.guild.id)]["member_role"])
            memberRole_id = guilddbRef.get().to_dict()['member_role']
            print(memberRole_id)
            memberRole = member.guild.get_role(int(memberRole_id))
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
            # roomOwnerRole1 = await member.guild.create_role(name=f"{member.display_name}の部屋の主", permissions=perms1)
            # await member.add_roles(roomOwnerRole1)
            # cat1 = bot.get_channel(guildsettings[str(member.guild.id)]["vc_category"])
            catVc = after.channel.category
            vc1 = await member.guild.create_voice_channel(f"（猥・工）{member.display_name}の部屋",
                                                          overwrites={role1: perm1, memberRole: perm2,
                                                                      # roomOwnerRole1: roomOwnerPerm1,
                                                                      member.guild.default_role: PermissionOverwrite().from_pair(
                                                                          Permissions.none(),
                                                                          Permissions.all())},
                                                          category=catVc, user_limit=2)
            # vcRole[str(vc1.id)] = role1.id
            # await role1.edit(position=8)
            #
            vcRoleRef.update({
                str(vc1.id): role1.id
            })
            await member.add_roles(role1)
            await member.move_to(vc1)

        if str(after.channel.id) == str(guilddbRef.get().to_dict()['create_qm_2']):
            print("hit. qm_2")
            # await member.guild.system_channel.send("hit.")
            # memberRole = member.guild.get_role(997644021067415642)
            # memberRole = member.guild.get_role(guildsettings.get().to_dict()[str(member.guild.id)]["member_role"])
            memberRole_id = guilddbRef.get().to_dict()['member_role']
            memberRole = member.guild.get_role(int(memberRole_id))
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
            # roomOwnerRole1 = await member.guild.create_role(name=f"{member.display_name}の部屋の主", permissions=perms1)
            # await member.add_roles(roomOwnerRole1)
            # cat1 = bot.get_channel(guildsettings[str(member.guild.id)]["vc_category"])
            catVc = after.channel.category
            vc1 = await member.guild.create_voice_channel(f"（寝）{member.display_name}の部屋",
                                                          overwrites={role1: perm1, memberRole: perm2,
                                                                      # roomOwnerRole1: roomOwnerPerm1,
                                                                      member.guild.default_role: PermissionOverwrite().from_pair(
                                                                          Permissions.none(),
                                                                          Permissions.all())},
                                                          category=catVc, user_limit=2)
            # vcRole[str(vc1.id)] = role1.id
            # await role1.edit(position=8)
            #
            vcRoleRef.update({
                str(vc1.id): role1.id
            })
            await member.add_roles(role1)
            await member.move_to(vc1)

    except:
        pass

    try:
        if str(after.channel.id) in vcRoleRef.get().to_dict().keys() and after.channel != before.channel:
            role1_id = vcRoleRef.get().to_dict()[str(after.channel.id)]
            role1 = after.channel.guild.get_role(int(role1_id))
            await member.add_roles(role1)
            # await member.add_roles()
            # await after.channel.send()
            prof_channel_id = guilddbRef.get().to_dict()['profile_channel']
            prof_channel = member.guild.get_channel(int(prof_channel_id))
            profiless = await prof_channel.history(limit=1000).flatten()
            for x in profiless:
                if x.author.id == member.id:
                    await after.channel.send(x.content)
            # await after.channel.send(view=MyViewMenu())
            from cogs.menu import MyViewMenu
            await after.channel.send(view=MyViewMenu())
            await after.channel.send(embed=Embed(description='Created by Yuki.'))
            await after.channel.send(member.mention)
            return
    except:
        pass
    if before.channel is not None and len(before.channel.members) == 0:
        print('vcRole:', vcRoleRef.get().to_dict())
        # vcRoleDic = vcRoleRef.get()
        vcRoleDic = vcRoleRef.get()

        var = vcRoleDic.to_dict()[str(before.channel.id)]
        print(var)
        role1 = member.guild.get_role(int(var))

        await role1.delete()
        var1 = vcRoleRef.get().to_dict()
        var1.pop(str(before.channel.id))
        print(var1)
        var2 = vcRoleRef.set(var1)
        print(var2)
        # vcRoleRef.delete()
        if var is not None:
            await before.channel.delete()


@bot.slash_command(description="自己紹介を表示")
async def prof(ctx: ApplicationContext, name: Option(str, required=True, description="名前")):
    # global vcRole
    # global vcTxt
    # global txtMsg
    # global guildsettings
    global db
    # prof_channel_id = guildsettings[str(ctx.guild.id)]["prof_channel"]
    prof_channel_id = db.collection(str(ctx.guild.id)).document('settings').get().to_dict()['profile_channel']
    prof_channel = bot.get_channel(int(prof_channel_id))
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
        if name in x.author.display_name:
            # await ctx.send_followup(x.content, delete_after=3 * 60, ephemeral=True)
            tosendmsg = tosendmsg + "\n" + x.content
            print(f"{x.author.name}: {x.content}")
    if tosendmsg == "":
        tosendmsg = "該当なし"
    await ctx.respond(embed=Embed(description=tosendmsg), delete_after=3 * 60, ephemeral=True)


# @bot.slash_command(name="close", description="この部屋に入れる人を限定する。")
# async def close(ctx: ApplicationContext):
#     global vcRole
#     global vcTxt
#     global txtMsg
#     global guildsettings
#     # try:
#     #     vcTxt[str(ctx.author.voice.channel.id)]
#     # except:
#     #     return
#     if not str(ctx.author.voice.channel.id) in vcTxt.keys():
#         print(traceback.format_exc())
#         return
#     vc1 = ctx.author.voice.channel
#     role1 = ctx.guild.get_role(vcRole[str(ctx.author.voice.channel.id)])
#     perm1 = PermissionOverwrite().from_pair(Permissions.advanced().general().voice(), Permissions.none())
#     perm2 = PermissionOverwrite().from_pair(Permissions.general(), Permissions.text())
#     # perm2.update(connect=True)
#     # perm2.update(speak=True)
#     # perm2.update(use_slash_commands=True)
#     perm2.update(connect=True)
#     perm2.update(speak=True)
#     # perm1.update(value=689379286592)
#     perm1.update(read_message_history=True)
#     perm1.update(read_messages=True)
#     perm1.update(send_messages=True)
#     perm1.update(use_slash_commands=True)
#     perm1.update(connect=True, speak=True)
#     perms1 = Permissions.advanced().general().voice()
#     perm1.update(mute_members=False)
#     perm1.update(move_members=False, deafen_members=False)
#     perms1.update(mute_members=False, move_members=False, deafen_members=False, connect=True, speak=True)
#     # memberRole = message.author.guild.get_role(997644021067415642)
#     memberRole = ctx.guild.get_role(guildsettings[str(ctx.guild.id)]["member_role"])
#     memberPerm = PermissionOverwrite().from_pair(Permissions.advanced().general(), Permissions.all())
#     memberPerm.update(view_channel=True)
#     await vc1.edit(overwrites={role1: perm1,
#                                memberRole: memberPerm,
#                                ctx.guild.default_role: PermissionOverwrite().from_pair(
#                                    Permissions.none(),
#                                    Permissions.all())
#                                }
#                    )
#     await ctx.respond(embed=Embed(description="完了."))
#
#
# @bot.slash_command(description="この部屋の名前を変える.")
# async def name(ctx: ApplicationContext, name: Option(str, description="名前", required=True)):
#     global vcRole
#     global vcTxt
#     global txtMsg
#     global guildsettings
#     try:
#         txt1 = vcTxt[str(ctx.author.voice.channel.id)]
#         txt1 = bot.get_channel(txt1)
#     except:
#         print(traceback.format_exc())
#         return
#     await txt1.edit(name=name)
#     vc1 = ctx.author.voice.channel
#     await vc1.edit(name=name)
#     await ctx.respond(embed=Embed(description="完了."))
#
#
# @bot.slash_command(description="部屋の人数制限を変える")
# async def limit(ctx: ApplicationContext, lim: Option(int, description="人数", required=True)):
#     global vcRole
#     global vcTxt
#     global txtMsg
#     global guildsettings
#     try:
#         txt1 = vcTxt[str(ctx.author.voice.channel.id)]
#         txt1 = bot.get_channel(txt1)
#     except:
#         print(traceback.format_exc())
#         return
#     await ctx.author.voice.channel.edit(user_limit=int(lim))
#     await ctx.respond(embed=Embed(description="完了."))
#
#
# @bot.slash_command(description="この部屋を見えなくする。")
# async def nolook(ctx: ApplicationContext):
#     global vcRole
#     global vcTxt
#     global txtMsg
#     global guildsettings
#     try:
#         vcTxt[str(ctx.author.voice.channel.id)]
#     except:
#         print(traceback.format_exc())
#         return
#     vc1 = ctx.author.voice.channel
#     role1 = ctx.guild.get_role(vcRole[str(ctx.author.voice.channel.id)])
#     perm1 = PermissionOverwrite().from_pair(Permissions.advanced().general().voice(), Permissions.none())
#     perm2 = PermissionOverwrite().from_pair(Permissions.general(), Permissions.text())
#     # perm2.update(connect=True)
#     # perm2.update(speak=True)
#     # perm2.update(use_slash_commands=True)
#     perm2.update(connect=True)
#     perm2.update(speak=True)
#     # perm1.update(value=689379286592)
#     perm1.update(read_message_history=True)
#     perm1.update(read_messages=True)
#     perm1.update(send_messages=True)
#     perm1.update(use_slash_commands=True)
#     perm1.update(connect=True, speak=True)
#     perms1 = Permissions.advanced().general().voice()
#     perm1.update(mute_members=False)
#     perm1.update(move_members=False, deafen_members=False)
#     perms1.update(mute_members=False, move_members=False, deafen_members=False, connect=True, speak=True)
#     # memberRole = message.author.guild.get_role(997644021067415642)
#     memberRole = ctx.guild.get_role(guildsettings[str(ctx.guild.id)]["member_role"])
#     memberPerm = PermissionOverwrite().from_pair(Permissions.advanced().none(), Permissions.all())
#     await vc1.edit(overwrites={
#         role1: perm1,
#         memberRole: memberPerm,
#         ctx.guild.default_role: PermissionOverwrite().from_pair(
#             Permissions.none(),
#             Permissions.all())}
#     )
#     await ctx.respond(embed=Embed(description="完了."))
#

# @bot.slash_command(description="この部屋を見えるようにする。")
# async def look(ctx: ApplicationContext):
#     global vcRole
#     global vcTxt
#     global txtMsg
#     global guildsettings
#     try:
#         vcTxt[str(ctx.author.voice.channel.id)]
#     except:
#         print(traceback.format_exc())
#         return
#     vc1 = ctx.author.voice.channel
#     role1 = ctx.guild.get_role(vcRole[str(ctx.author.voice.channel.id)])
#     perm1 = PermissionOverwrite().from_pair(Permissions.advanced().general().voice(), Permissions.none())
#     perm2 = PermissionOverwrite().from_pair(Permissions.general(), Permissions.text())
#     # perm2.update(connect=True)
#     # perm2.update(speak=True)
#     # perm2.update(use_slash_commands=True)
#     perm2.update(connect=True)
#     perm2.update(speak=True)
#     # perm1.update(value=689379286592)
#     perm1.update(read_message_history=True)
#     perm1.update(read_messages=True)
#     perm1.update(send_messages=True)
#     perm1.update(use_slash_commands=True)
#     perm1.update(connect=True, speak=True)
#     perms1 = Permissions.advanced().general().voice()
#     perm1.update(mute_members=False)
#     perm1.update(move_members=False, deafen_members=False)
#     perms1.update(mute_members=False, move_members=False, deafen_members=False, connect=True, speak=True)
#     # perm1 = PermissionOverwrite().from_pair(Permissions.advanced().general().voice(), Permissions.none())
#     memberRole = ctx.guild.get_role(guildsettings[str(ctx.guild.id)]["member_role"])
#     memberPerm = PermissionOverwrite().from_pair(Permissions.general(), Permissions.text())
#     # perm2.update(connect=True)
#     # perm2.update(speak=True)
#     # perm2.update(use_slash_commands=True)
#     memberPerm.update(connect=True)
#     memberPerm.update(speak=True)
#     # memberRole = message.author.guild.get_role(997644021067415642)
#     # memberRole = ctx.guild.get_role(guildsettings[str(ctx.guild.id)]["member_role"])
#     # memberPerm = PermissionOverwrite().from_pair(Permissions.advanced().none(), Permissions.all())
#     await vc1.edit(overwrites={
#         role1: perm1,
#         memberRole: memberPerm,
#         ctx.guild.default_role: PermissionOverwrite().from_pair(
#             Permissions.none(),
#             Permissions.all())}
#     )
#     await ctx.respond(embed=Embed(description="完了."))
#

@bot.slash_command()
async def ping(ctx: ApplicationContext):
    lat = bot.latency
    await ctx.respond(embed=Embed(description=f"レイテンシーは、{lat * 60}ms."))


bot.run(TOKEN)
