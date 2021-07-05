import inspect
import os
import yaml
import logging

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from Utils.classes import Command, Group
from Utils import permissions
from Utils import colours

with open("config.yml", "r") as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)

with open("bot.yml", "r") as ymlfile:
    bot = yaml.load(ymlfile, Loader=yaml.FullLoader)

if bot["dev"]:
    TOKEN = bot["dev_token"]
    PREFIX = config["prefix"] + config["prefix"]

else:
    TOKEN = bot["token"]
    PREFIX = config["prefix"]

intents = discord.Intents.default()
intents.members = True
intents.presences = True

activity = discord.Activity(name='with the devs!', type=discord.ActivityType.playing)
client = Bot(command_prefix=PREFIX, help_command=None, owner_id=278548721778688010, activity=activity, intents=intents)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# Global Check
@client.check
async def dev_mode(ctx):
    if bot["dev"]:
        return permissions.BotAdminCheck(ctx)
    return True


@permissions.BotAdmin()
@client.group(name='cog',
              usage='cog [load/unload/reload]',
              invoke_without_command=True,
              description='Loads/Unloads/Reloads a cog.',
              cls=Group,
              access='botAdmin')
async def cog(context):
    raise commands.MissingRequiredArgument(inspect.Parameter('UsageError', inspect.Parameter.POSITIONAL_ONLY))


@permissions.BotAdmin()
@cog.command(name='load', usage='cog load [cog]', description='Load a cog.', cls=Command, access='botAdmin')
async def load(context, *, extension):
    extension = extension.title()
    try:
        client.load_extension(f'Cogs.{extension}')
        embed = discord.Embed(description=f'{extension} Loaded!', colour=config['embed']['colour'])
        embed.set_footer(text=config['embed']['footer']['text'], icon_url=config['embed']['footer']['url'])
        await context.send(embed=embed)
    except Exception as error2:
        embed = discord.Embed(description=f'{extension} cannot be loaded.', colour=config['embed']['colour'])
        embed.set_footer(text=config['embed']['footer']['text'], icon_url=config['embed']['footer']['url'])
        await context.send(embed=embed)

    print(f'{extension} loaded.')


@permissions.BotAdmin()
@cog.command(name='unload', usage='cog unload [cog]', description='Unload a cog.', cls=Command, access='botAdmin')
async def unload(context, extension):
    extension = extension.title()
    try:
        client.unload_extension(f'Cogs.{extension}')
        embed = discord.Embed(description=f'{extension} Unloaded!', colour=config['embed']['colour'])
        embed.set_footer(text=config['embed']['footer']['text'], icon_url=config['embed']['footer']['url'])
        await context.send(embed=embed)
    except Exception as error2:
        embed = discord.Embed(description=f'{extension} cannot be unloaded.', colour=config['embed']['colour'])
        embed.set_footer(text=config['embed']['footer']['text'], icon_url=config['embed']['footer']['url'])
        await context.send(embed=embed)

    print(f'{extension} unloaded.')


@permissions.BotAdmin()
@cog.command(name='reload', usage='command reload [command]', description='Reload a cog.', cls=Command, access='botAdmin')
async def reload(context, extension):
    extension = extension.title()
    try:
        client.unload_extension(f'Cogs.{extension}')
        client.load_extension(f'Cogs.{extension}')
        embed = discord.Embed(description=f'{extension} Reloaded!', colour=config['embed']['colour'])
        embed.set_footer(text=config['embed']['footer']['text'], icon_url=config['embed']['footer']['url'])
        await context.send(embed=embed)
    except Exception as error2:
        embed = discord.Embed(description=f'{extension} cannot be reloaded.', colour=config['embed']['colour'])
        embed.set_footer(text=config['embed']['footer']['text'], icon_url=config['embed']['footer']['url'])
        await context.send(embed=embed)
    print(f'{extension} reloaded.')


@permissions.Access(11)
@client.command(name='level', usage='level', cls=Command, description='Does some magic shit', access=None)
async def level(context):
    await context.send('You just did the impossible...')


dontLoad = []

if __name__ == '__main__':
    for i in os.listdir('Cogs'):
        if i.endswith('.py') and i not in dontLoad:
            try:
                client.load_extension(f'Cogs.{i[:-3]}')
                print(f'{colours.OKGREEN}{i[:-3]} loaded.\033[0m')

            except Exception as error:
                print(f'{colours.FAIL}{i[:-3]} cannot be loaded. [{error}]')

client.run(TOKEN)
