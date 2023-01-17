from discord import *
from google.cloud import firestore
from firestore import *

class Ticket(Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
