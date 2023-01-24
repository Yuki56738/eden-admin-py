from discord import *
from google.cloud import firestore


# from google.cloud
class CreateVC(Cog):
    def __init__(self, bot):
        self.bot = bot
        # self._last_member = None

    @Cog.listener()
    async def on_ready(self):
        print('create_vc.py loaded.')

    @Cog.listener()
    # async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState):
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        await self.bot.wait_until_ready()
        db = firestore.Client()
        guilddbRef = db.collection(str(member.guild.id)).document('settings')
        vcRoleRef = db.collection(str(member.guild.id)).document('vcRole')
        # vcTxtRef = db.collection(str(member.guild.id)).document('vcTxt')
        create_vc_channel_id = guilddbRef.get().to_dict()['create_vc_channel']
        print('create_vc_channel_id:', create_vc_channel_id)
        create_vc_channel = member.guild.get_channel(create_vc_channel_id)
        # try:
        if str(after.channel.id) == str(create_vc_channel_id):
            print("hit.")
            # await member.guild.system_channel.send("hit.")
            # memberRole = member.guild.get_role(997644021067415642)
            # memberRole = member.guild.get_role(guildsettings.get().to_dict()[str(member.guild.id)]["member_role"])
            memberRole_id = guilddbRef.get().to_dict()['member_role']
            print('memberRole_id:', memberRole_id)

            memberRole = member.guild.get_role(memberRole_id)
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
            self.bot: Bot
            thisguild = self.bot.get_guild(member.guild.id)
            await member.add_roles(role1)
            vc1 = await thisguild.create_voice_channel(name=f"{member.display_name}の部屋",
                                                       overwrites={role1: perm1, memberRole: perm2,
                                                                   # roomOwnerRole1: roomOwnerPerm1,
                                                                   member.guild.default_role: PermissionOverwrite().from_pair(
                                                                       Permissions.none(),
                                                                       Permissions.all())},
                                                       category=catVc, user_limit=2)
            # vcRole[str(vc1.id)] = role1.id
            # await role1.edit(position=8)
            #
            if not vcRoleRef.get().exists:
                vcRoleRef.create({
                    str(vc1.id): role1.id
                })
            else:
                vcRoleRef.update({
                    str(vc1.id): role1.id
                })
            await member.add_roles(role1)
            await member.move_to(vc1)
            # txt1 = await member.guild.create_text_channel(name=f"{member.display_name}の部屋",
            #                                               overwrites={role1: perm1, roomOwnerRole1: roomOwnerPerm1,
            #                                                           member.guild.default_role: PermissionOverwrite().from_pair(
            #                                                               Permissions.none(),
            #                                                               Permissions.all())},
            #                                               category=catVc)
            #
            # vcTxt[str(vc1.id)] = txt1.id
            # vcOwnerRole[str(vc1.id)] = roomOwnerRole1.id

            msgToSend = """
        ted by Yuki.
        e [名前] で部屋の名前を変える
        ame  私のおうち
        it [人数] で部屋の人数制限を変える
        imit 4（半角
        se でこの部屋に入れる人を限定する。「返信」にてメンションされた人は入れるようになる。
        ook でこの部屋を見えなくする。
        k で、この部屋を見えるようにする。

        u で、メニューを表示。"""
            # embedToSend = Embed(description=msgToSend)
            # msgDescript = await txt1.send(embed=Embed(description=msgToSend))
            #
            # await txt1.send(view=MyViewChangeRoomName())
            # await txt1.send(view=MyViewChangeRoomLimit())
            # await txt1.send(view=MyViewRoomNolook())

            # ここにボタン等を配置
            # await msgDescript.add_reaction()
            # emoji = '👍'
            # await msgDescript.add_reaction(emoji)
            # msgToSend2 = ""
            # try:
            #     # prof_channel = bot.get_channel(995656569301774456)
            #     prof_channel_id = guildsettings[str(member.guild.id)]["prof_channel"]
            #     prof_channel = bot.get_channel(prof_channel_id)
            #     prof_messages = await prof_channel.history(limit=1000).flatten()
            #     for x in prof_messages:
            #         if x.author.id == member.id:
            #             # await txt1.send(x.content)
            #             # await txt1.send(embed=Embed(description=x.content))
            #             msgToSend2 += x.content
            #             await vc1.send(embed=Embed(description=msgToSend2))
            # except:
            #     # print(traceback.format_exc())
            #     traceback.print_exc()
            # msgToSend2 += member.mention
            ##
            # prof_channel_id = 995656569301774456
            # prof_channel = member.guild.get_channel(prof_channel_id)
            # profiless = await prof_channel.history(limit=1000).flatten()
            # for x in profiless:
            #     if x.author.id == member.id:
            #         await vc1.send(x.content)
            # print(profiless)
            ##
            await vc1.send(member.mention)
            # await txt1.send(embed=Embed(description=msgToSend2))
            # save_to_json()
            return
        # except:
        #     pass
        # if not after.channel is None and after.channel.id == guildsettings[str(member.guild.id)]["create_vc_channel_qm_general"]:
        #     try:
        #         if after.channel.id == guildsettings[str(member.guild.id)]["create_vc_channel_qm_general"]:
        #             print("qm_general hit.")
        #             # await member.guild.system_channel.send("hit.")
        #             # memberRole = member.guild.get_role(997644021067415642)
        #             memberRole = member.guild.get_role(guildsettings[str(member.guild.id)]["member_role"])
        #             # perm1 = PermissionOverwrite().from_pair(Permissions.general(), Permissions.none())
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
        #             perm1.update(move_members=False, deafen_members=False, attach_files=True, embed_links=True)
        #             perms1.update(mute_members=False, move_members=False, deafen_members=False, connect=True, speak=True)
        #             # perms1.update(connect=True, speak=True)
        #             role1 = await member.guild.create_role(name=f"（雑・作）{member.display_name}の部屋", permissions=perms1)
        #             # cat1 = bot.get_channel(guildsettings[str(member.guild.id)]["vc_category"])
        #             catVc = after.channel.category
        #             # cat2 = bot.get_channel(guildsettings[str(member.guild.id)]["vc_category"])
        #             vc1 = await member.guild.create_voice_channel(f"（雑・作）{member.display_name}の部屋",
        #                                                           overwrites={role1: perm1,
        #                                                                       memberRole: perm2,
        #                                                                       member.guild.default_role: PermissionOverwrite().from_pair(
        #                                                                           Permissions.none(),
        #                                                                           Permissions.all())
        #                                                                       },
        #                                                           category=catVc, user_limit=2)
        #             vcRole[str(vc1.id)] = role1.id
        #             # await role1.edit(position=8)
        #             await member.add_roles(role1)
        #             await member.move_to(vc1)
        #             txt1 = await member.guild.create_text_channel(name=f"（雑・作）{member.display_name}の部屋",
        #                                                           overwrites={role1: perm1,
        #                                                                       member.guild.default_role: PermissionOverwrite().from_pair(
        #                                                                           Permissions.none(),
        #                                                                           Permissions.all())},
        #                                                           category=catVc)
        #             vcTxt[str(vc1.id)] = txt1.id
        #             msgToSend = """
        #             Created by Yuki.
        #             /name [名前] で部屋の名前を変える
        #             例｜/name  私のおうち
        #             /limit [人数] で部屋の人数制限を変える
        #             例｜/limit 4（半角
        #             /close でこの部屋に入れる人を限定する。「返信」にてメンションされた人は入れるようになる。
        #             /nolook でこの部屋を見えなくする。
        #             /look で、この部屋を見えるようにする。
        #
        #             /menu で、メニューを表示。"""
        #             # embedToSend = Embed(description=msgToSend)
        #             msgDescript = await txt1.send(embed=Embed(description=msgToSend))
        #
        #             await txt1.send(view=MyViewChangeRoomName())
        #             await txt1.send(view=MyViewChangeRoomLimit())
        #             # await txt1.send(view=MyViewRoomNolook())
        #
        #             # ここにボタン等を配置
        #             # await msgDescript.add_reaction()
        #             # emoji = '👍'
        #             # await msgDescript.add_reaction(emoji)
        #             msgToSend2 = ""
        #             try:
        #                 # prof_channel = bot.get_channel(995656569301774456)
        #                 prof_channel_id = guildsettings[str(member.guild.id)]["prof_channel"]
        #                 prof_channel = bot.get_channel(prof_channel_id)
        #                 prof_messages = await prof_channel.history(limit=1000).flatten()
        #                 for x in prof_messages:
        #                     if x.author.id == member.id:
        #                         # await txt1.send(x.content)
        #                         # await txt1.send(embed=Embed(description=x.content))
        #                         msgToSend2 += x.content
        #                         await txt1.send(embed=Embed(description=msgToSend2))
        #             except:
        #                 # print(traceback.format_exc())
        #                 traceback.print_exc()
        #             # msgToSend2 += member.mention
        #             await txt1.send(member.mention)
        #             # await txt1.send(embed=Embed(description=msgToSend2))
        #             # save_to_json()
        #     except:
        #         pass
        #     try:
        #         if after.channel.id == guildsettings[str(member.guild.id)]["create_vc_channel_qm_1"]:
        #             print("qm_1 hit.")
        #             # await member.guild.system_channel.send("hit.")
        #             # memberRole = member.guild.get_role(997644021067415642)
        #             memberRole = member.guild.get_role(guildsettings[str(member.guild.id)]["member_role"])
        #             # perm1 = PermissionOverwrite().from_pair(Permissions.general(), Permissions.none())
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
        #             perm1.update(move_members=False, deafen_members=False, attach_files=True, embed_links=True)
        #             perms1.update(mute_members=False, move_members=False, deafen_members=False, connect=True, speak=True)
        #             # perms1.update(connect=True, speak=True)
        #             role1 = await member.guild.create_role(name=f"（猥・エ）{member.display_name}の部屋", permissions=perms1)
        #             # cat1 = bot.get_channel(guildsettings[str(member.guild.id)]["vc_category"])
        #             # cat2 = after.channel.category
        #             cat2 = bot.get_channel(guildsettings[str(member.guild.id)]["vc_category"])
        #             catVc = after.channel.category
        #             vc1 = await member.guild.create_voice_channel(f"（猥・エ）{member.display_name}の部屋", overwrites={role1: perm1,
        #                                                                                                            memberRole: perm2,
        #                                                                                                            member.guild.default_role: PermissionOverwrite().from_pair(
        #                                                                                                                Permissions.none(),
        #                                                                                                                Permissions.all())
        #                                                                                                            },
        #                                                           category=catVc, user_limit=2)
        #             vcRole[str(vc1.id)] = role1.id
        #             # await role1.edit(position=8)
        #             await member.add_roles(role1)
        #             await member.move_to(vc1)
        #             txt1 = await member.guild.create_text_channel(name=f"（猥・エ）{member.display_name}の部屋",
        #                                                           overwrites={role1: perm1,
        #                                                                       member.guild.default_role: PermissionOverwrite().from_pair(
        #                                                                           Permissions.none(),
        #                                                                           Permissions.all())},
        #                                                           category=catVc)
        #             vcTxt[str(vc1.id)] = txt1.id
        #             msgToSend = """
        # Created by Yuki.
        # /name [名前] で部屋の名前を変える
        # 例｜/name 私のおうち
        # /limit [人数] で部屋の人数制限を変える
        # 例｜/limit 4（半角
        # /close でこの部屋に入れる人を限定する。「返信」にてメンションされた人は入れるようになる。
        # /nolook でこの部屋を見えなくする。
        # /look で、この部屋を見えるようにする。
        #
        # /menu で、メニューを表示。"""
        #             # embedToSend = Embed(description=msgToSend)
        #             msgDescript = await txt1.send(embed=Embed(description=msgToSend))
        #
        #             await txt1.send(view=MyViewChangeRoomName())
        #             await txt1.send(view=MyViewChangeRoomLimit())
        #             # await txt1.send(view=MyViewRoomNolook())
        #
        #             # ここにボタン等を配置
        #             # await msgDescript.add_reaction()
        #             # emoji = '👍'
        #             # await msgDescript.add_reaction(emoji)
        #             msgToSend2 = ""
        #             try:
        #                 # prof_channel = bot.get_channel(995656569301774456)
        #                 prof_channel_id = guildsettings[str(member.guild.id)]["prof_channel"]
        #                 prof_channel = bot.get_channel(prof_channel_id)
        #                 prof_messages = await prof_channel.history(limit=1000).flatten()
        #                 for x in prof_messages:
        #                     if x.author.id == member.id:
        #                         # await txt1.send(x.content)
        #                         # await txt1.send(embed=Embed(description=x.content))
        #                         msgToSend2 += x.content
        #                         await txt1.send(embed=Embed(description=msgToSend2))
        #             except:
        #                 # print(traceback.format_exc())
        #                 traceback.print_exc()
        #             # msgToSend2 += member.mention
        #             await txt1.send(member.mention)
        #             # await txt1.send(embed=Embed(description=msgToSend2))
        #             # save_to_json()
        #     except:
        #         pass
        #     try:
        #         if after.channel.id == guildsettings[str(member.guild.id)]["create_vc_channel_qm_2"]:
        #             print("qm_2 hit.")
        #             # await member.guild.system_channel.send("hit.")
        #             # memberRole = member.guild.get_role(997644021067415642)
        #             memberRole = member.guild.get_role(guildsettings[str(member.guild.id)]["member_role"])
        #             # perm1 = PermissionOverwrite().from_pair(Permissions.general(), Permissions.none())
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
        #             perm1.update(move_members=False, deafen_members=False, attach_files=True, embed_links=True)
        #             perms1.update(mute_members=False, move_members=False, deafen_members=False, connect=True, speak=True)
        #             # perms1.update(connect=True, speak=True)
        #             role1 = await member.guild.create_role(name=f"（寝）{member.display_name}の部屋", permissions=perms1)
        #             # cat1 = bot.get_channel(guildsettings[str(member.guild.id)]["vc_category"])
        #             # cat2 = after.channel.category
        #             cat2 = bot.get_channel(guildsettings[str(member.guild.id)]["vc_category"])
        #             catVc = after.channel.category
        #             vc1 = await member.guild.create_voice_channel(f"（寝）{member.display_name}の部屋", overwrites={role1: perm1,
        #                                                                                                          memberRole: perm2,
        #                                                                                                          member.guild.default_role: PermissionOverwrite().from_pair(
        #                                                                                                              Permissions.none(),
        #                                                                                                              Permissions.all())
        #                                                                                                          },
        #                                                           category=catVc, user_limit=2)
        #             vcRole[str(vc1.id)] = role1.id
        #             # await role1.edit(position=8)
        #             await member.add_roles(role1)
        #             await member.move_to(vc1)
        #             txt1 = await member.guild.create_text_channel(name=f"（寝）{member.display_name}の部屋",
        #                                                           overwrites={role1: perm1,
        #                                                                       member.guild.default_role: PermissionOverwrite().from_pair(
        #                                                                           Permissions.none(),
        #                                                                           Permissions.all())},
        #                                                           category=catVc)
        #             vcTxt[str(vc1.id)] = txt1.id
        #             msgToSend = """
        #             Created by Yuki.
        #             /name [名前] で部屋の名前を変える
        #             例｜/name  私のおうち
        #             /limit [人数] で部屋の人数制限を変える
        #             例｜/limit 4（半角
        #             /close でこの部屋に入れる人を限定する。「返信」にてメンションされた人は入れるようになる。
        #             /nolook でこの部屋を見えなくする。
        #             /look で、この部屋を見えるようにする。
        #
        #             /menu で、メニューを表示。"""
        #             # embedToSend = Embed(description=msgToSend)
        #             msgDescript = await txt1.send(embed=Embed(description=msgToSend))
        #
        #             await txt1.send(view=MyViewChangeRoomName())
        #             await txt1.send(view=MyViewChangeRoomLimit())
        #             # await txt1.send(view=MyViewRoomNolook())
        #
        #             # ここにボタン等を配置
        #             # await msgDescript.add_reaction()
        #             # emoji = '👍'
        #             # await msgDescript.add_reaction(emoji)
        #             msgToSend2 = ""
        #             try:
        #                 # prof_channel = bot.get_channel(995656569301774456)
        #                 prof_channel_id = guildsettings[str(member.guild.id)]["prof_channel"]
        #                 prof_channel = bot.get_channel(prof_channel_id)
        #                 prof_messages = await prof_channel.history(limit=1000).flatten()
        #                 for x in prof_messages:
        #                     if x.author.id == member.id:
        #                         # await txt1.send(x.content)
        #                         # await txt1.send(embed=Embed(description=x.content))
        #                         msgToSend2 += x.content
        #                         await txt1.send(embed=Embed(description=msgToSend2))
        #             except:
        #                 # print(traceback.format_exc())
        #                 traceback.print_exc()
        #             # msgToSend2 += member.mention
        #             await txt1.send(member.mention)
        #             # await txt1.send(embed=Embed(description=msgToSend2))
        #             # save_to_json()
        #     except:
        #         pass
        # except:
        #     pass


def setup(bot):
    bot.add_cog(CreateVC(bot))
