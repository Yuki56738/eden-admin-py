from discord import *
#
# from main import MyViewMenu
from google.cloud import firestore

db = firestore.Client()

import discord


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


class MyViewMenu(discord.ui.View):
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

    @discord.ui.button(label='寝落ちした人を移動する')
    async def button4_callback(self, button, interaction: discord.Interaction):
        interaction.response: InteractionResponse
        from cogs.move import MyViewMoveMember
        await interaction.response.send_message(view=MyViewMoveMember())

    @discord.ui.button(label='プロフ検索', style=discord.ButtonStyle.blurple)
    async def button6_callback(self, button, interaction: Interaction):
        interaction.response: InteractionResponse
        await interaction.response.send_modal(MyModalSearchProf(title='対象の名前を入力...'))

class MyModalSearchProf(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="対象の名前を入力...", style=discord.InputTextStyle.singleline))

    async def callback(self, interaction: discord.Interaction):
        interaction.response: InteractionResponse
        prof_channel_id = db.collection(str(interaction.guild.id)).document('settings').get().to_dict()['profile_channel']
        prof_channel = interaction.guild.get_channel(int(prof_channel_id))
        prof_messages = await prof_channel.history(limit=1000).flatten()
        # await ctx.respond("自己紹介...", ephemeral=True, delete_after=3*60)
        # print(ctx.author.guild_permissions)
        tosendmsg = ""
        for x in prof_messages:
            # if x.author.id == xuser.id:
            if x.author.id == interaction.user.id:
                # await ctx.send_followup(x.content, delete_after=3 * 60, ephemeral=True)
                tosendmsg = tosendmsg + x.content
                print(f"{x.author.name}: {x.content}")

            # for xuser in ctx.author.voice.channel.members:
            #     if x.author.id == xuser.id and not ctx.author.id:
            #         print(x.content)
            #         # await ctx.send_followup(x.content, delete_after=3*60, ephemeral=True)
            #         tosendmsg = tosendmsg + x.content
            name = self.children[0].value
            if name in x.author.display_name:
                # await ctx.send_followup(x.content, delete_after=3 * 60, ephemeral=True)
                tosendmsg = tosendmsg + "\n" + x.content
                print(f"{x.author.name}: {x.content}")
        if tosendmsg == "":
            tosendmsg = "該当なし"
        interaction.response: InteractionResponse
        await interaction.response.send_message(embed=Embed(description=tosendmsg), delete_after=3 * 60, ephemeral=True)
        interaction.followup: Webhook
        await interaction.followup.send(embed=Embed(description=f'{interaction.user.mention} 結果を送信しました！\nご確認ください.'))
class MyViewMenu2(discord.ui.View):
    @discord.ui.button(label='寝落ちした人を移動する')
    async def button5_callback(self, button, interaction: discord.Interaction):
        interaction.response: InteractionResponse
        from cogs.move import MyViewMoveMember
        await interaction.response.send_message(view=MyViewMoveMember())
    @discord.ui.button(label='プロフ検索', style=discord.ButtonStyle.blurple)
    async def button6_callback(self, button, interaction: Interaction):
        interaction.response: InteractionResponse
        await interaction.response.send_modal(MyModalSearchProf(title='対象の名前を入力...'))

class Menu(Cog):
    def __init__(self, bot):
        self.bot = bot
        # self._last_member = None

    @Cog.listener()
    async def on_ready(self):
        print("Menu Cog ready.")

    @commands.slash_command(description='メニューを表示する.')
    async def menu(self, ctx: ApplicationContext):
        # from main import MyViewMenu
        global db
        vcRoleRef = db.collection(str(ctx.guild.id)).document('vcRole')
        if not str(ctx.channel_id) in vcRoleRef.get().to_dict().keys():
            await ctx.respond(view=MyViewMenu2())
            return
        await ctx.respond(view=MyViewMenu())


def setup(bot):
    bot.add_cog(Menu(bot))
