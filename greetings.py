from discord import *

class Greetings(Cog):
    def __init__(self, bot):
        self.bot = bot

        # self._last_member = None

    @Cog.listener()
    async def on_ready(self):
        print("ready.")
def setup(bot):
    bot.add_cog(Greetings(bot))