
from google.cloud import firestore
from google.cloud.firestore import *
import discord
from discord import *


class Ticket(Cog):
    def __init__(self, bot):
        self.bot = bot
        # asyncio.coroutine(self.bot.wait_until_ready)

        # bot.wait_until_ready()
        # print(bot1.guilds)
        # print(thisguildDoc.get().to_dict())
        # asyncio.run(self.onload)
        # async def onload(self):

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
            cat1 = interaction.guild.get_channel(cat1)
            # cat1 = guilddb1_dict[str(interaction.guild.id)]["ticket_category"]
            # cat1 = bot.get_channel(cat1)
            # cat1 = interaction.channel

            txt1: TextChannel = await interaction.guild.create_text_channel(
                name=f"{interaction.user.display_name}のticket",
                category=cat1,
                overwrites={
                    interaction.guild.default_role: permow2,
                    interaction.user: permow1
                })

            # db = firestore.Client()
            # db1 = db.collection("guilddb").document(document_id="ticketTxtUser")
            # db1_dict = db1.get().to_dict()
            # if db1_dict is None:
            #     db1_dict1 = {
            #         str(txt1.id): str(interaction.user.id)
            #     }
            #     db1.create(db1_dict1)
            #
            # db1_dict[str(txt1.id)] = str(interaction.user.id)
            # print(db1.update(db1_dict))
            # db1.update(db1_dict)
            await txt1.send(f"問題が作成されました。ただいま対応しますので、少々お待ちください... {interaction.user.mention}")


    @commands.slash_command()
    async def ticket(self, ctx: ApplicationContext):
        print("ready ticket.")

        # for x in self.bot.guilds:
        #     print(x.id, x.name)

        # db = firestore.Client()
        # guilddbCol = db.collection("guilddb")
        # guildsettingsDoc_ref = guilddbCol.document("guildsettings")
        # thisguildCol_ref: CollectionReference = guildsettingsDoc_ref.collection(str(x.id))
        # thisguildDoc = thisguildCol_ref.document(document_id="ticket_channel")
        # # print(thisguildDoc.get().to_dict()["id"])
        # ticket_channel_id = int(thisguildDoc.get().to_dict()["id"])
        db = firestore.Client()
        guilddb = db.collection("guilddb")
        guilddb1 = guilddb.document(document_id="guildsettings")
        guilddb1_dict = guilddb1.get().to_dict()
        ticket_channel_id = guilddb1_dict[str(ctx.guild.id)]['ticket_channel']
        self.bot: Bot
        ticket_channel = self.bot.get_channel(ticket_channel_id)
        await ticket_channel.send(view=self.MyViewTicket())

    @commands.slash_command(description="ticketのDBを初期化")
    async def init_ticket(self, ctx: ApplicationContext, ticket_channel_id: str):
        if not ctx.user.guild_permissions.administrator:
            await ctx.respond("管理者のみ使用できます.")
            return
        await ctx.respond("頑張っています...")
        # db = firestore.Client()
        # guilddbCol = db.collection("guilddb")
        # guildsettingsDoc_ref = guilddbCol.document("guildsettings")
        # thisguildCol_ref: CollectionReference = guildsettingsDoc_ref.collection(str(ctx.guild.id))
        #
        # thisguildDoc = thisguildCol_ref.document(document_id="ticket_channel")
        db = firestore.Client()
        guilddb = db.collection("guilddb")
        guilddb1 = guilddb.document(document_id="guildsettings")
        guilddb1_dict = guilddb1.get().to_dict()
        guilddb1_dict[str(ctx.guild.id)]['ticket_channel'] = ticket_channel_id
        # print(thisguildDoc.get().to_dict())
        # thisguildDoc.set({
        #     "id": str(ctx.guild.get_channel(int(ticket_channel_id)).id),
        #     "name": str(ctx.guild.get_channel(int(ticket_channel_id)).name)
        # })
        guilddb1.set(document_data=guilddb1_dict)
        await ctx.send("完了.")


def setup(bot):
    bot.add_cog(Ticket(bot))
