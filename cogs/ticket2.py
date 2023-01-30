from discord import *
# from discord_buttons_plugin import *


class Ticket2(Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.buttons = ButtonsClient(bot=self.bot)

        # self._last_member = None

    @commands.slash_command()
    async def ticket(self, ctx: ApplicationContext):
        # await ctx.respond()


    # await but

    @Cog.listener()
    async def on_ready(self):
        print("Ticket2 ready.")


def setup(bot):
    bot.add_cog(Ticket2(bot))
