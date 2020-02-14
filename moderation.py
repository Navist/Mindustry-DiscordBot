import discord
from discord.ext import commands
from discord.ext import tasks
import asyncio
import json
import socket

config = {}


with open('config.json', 'r') as f:
    config = json.load(f)

notAllowed = config['notAllowed']
modRoles = config["modRoles"]
owner = config['owner']
host = config['host']
port = config['port']
absolutelyNotAllowed = config['absolutelyNotAllowed']


class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def permissionsChecker(self, ctx):
        author = ctx.message.author
        for role in author.roles:
            if str(role.id) in modRoles:
                return True

    @commands.command(name='console', pass_context=True, help='Runs commands to the servers console through the open socket.')
    async def console(self, ctx, *command):
        author = ctx.message.author
        moderator = await self.permissionsChecker(ctx)
        print(moderator)
        if len(notAllowed) == 0:
            await ctx.send("This command is not available for use until you've configured the notAllowed list inside the config.json.")
            return
        for x in absolutelyNotAllowed:
            if x in command and str(author.id) != owner:
                await ctx.message.delete()
                msg = await ctx.send("{}, You do not have permission to use this command.".format(author.mention))
                await asyncio.sleep(4)
                await msg.delete()
                return
        for x in notAllowed: 
            if x in command and str(author.id) != owner and moderator != True:
                await ctx.message.delete()
                msg = await ctx.send("{}, You do not have permission to use this command.".format(author.mention))
                await asyncio.sleep(4)
                await msg.delete()
                return
        command = " ".join(command)
        command = '{}\n'.format(command).encode()
        returnMessage = []
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(2)
                server_address = (host, int(port))
                sock.connect(server_address)
                sock.send(command)
                while True:
                    msg = sock.recv(1024)
                    returnMessage.append(msg.decode())
        except socket.timeout:
            lengthReturn = len(returnMessage)
            while lengthReturn != 0:
                sendOne = "".join(returnMessage[0:4])
                del returnMessage[0:4]
                lengthReturn = len(returnMessage)
                if len(sendOne) == 0:
                    pass
                else:
                    await ctx.send(sendOne)
            await ctx.send("Console readout complete.")


def setup(client):
    client.add_cog(moderation(client))