from datetime import datetime

from discord import *

class Event(Cog):
    def __init__(self, bot):
        self.bot = bot

        # self._last_member = None
    @commands.slash_command()
    async def event(self, ctx: ApplicationContext):
        await ctx.respond("event command hit.")
        await ctx.guild.create_scheduled_event(name="an event", description="a test event", start_time=datetime.strptime("19:00"))
    @Cog.listener()
    async def on_ready(self):
        print("ready.")
def setup(bot):
    bot.add_cog(Event(bot))