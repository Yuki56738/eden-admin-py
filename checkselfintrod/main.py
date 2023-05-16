import os

import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    # checkchannel = client.get_channel(965426636436697088)
    checkguild = client.get_guild(965354369556049990)
    checkchannel = checkguild.get_channel(965426636436697088)
    guildmembers = checkguild.members
    writtenmembers = []
    # newwrittenmembers = []
    i = 0
    async for msg in checkchannel.history(limit=10000):
        writtenmembers.append(msg.author)
        if msg.author == client.user:
            # print(msg.content)
            y = msg.content.replace("<@","").replace(">", "")
            # print(y[0:18])
            z = y[0:18]
            a = checkguild.get_member(int(z))
            # print(a.name)
            writtenmembers.append(a)
        i += 1
    notwritenmembers = []
    for x in guildmembers:
        if not x in writtenmembers:
            print(x.name)
            if not x.bot:
                notwritenmembers.append(x.name)
    with open('result.txt', 'w')as f:
        for x in notwritenmembers:
            f.write(x)
            f.write('\n')


client.run(os.environ.get("DISCORD_TOKEN"))
