import discord
import string
import random
import yaml
import requests

from .database import insert, update, fetch
from discord.ext import commands

with open("config.yml", "r") as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)

with open("bot.yml", "r") as ymlfile:
    bot = yaml.load(ymlfile, Loader=yaml.FullLoader)


class NoPermission(commands.CheckFailure):
    pass


def Access(permissionLevel: int = 10):
    async def predicate(ctx):
        highest = 0

        result = fetch(f'SELECT * FROM PermissionOverride WHERE id = "{ctx.message.author.id}"')

        if result:
            if result[0][1] >= permissionLevel:
                return result[0][1] >= permissionLevel
            else:
                highest = result[0][1]

        result = fetch(
            f'SELECT * FROM UserPermissions WHERE guildId = "{ctx.message.channel.guild.id}" AND id = "{ctx.message.author.id}"')

        if result:
            if result[0][1] >= permissionLevel:
                return result[0][1] >= permissionLevel
            else:
                highest = result[0][1]

        result2 = fetch(
            f'SELECT * FROM RolePermissions WHERE guildId = "{ctx.message.channel.guild.id}" AND permissionLevel >= "{permissionLevel}"')

        for i in result2:
            role = discord.utils.get(ctx.guild.roles, id=i[0])
            if role in ctx.author.roles:
                return True

        result3 = fetch(f'SELECT * FROM RolePermissions WHERE guildId = "{ctx.message.channel.guild.id}"')

        for i in result3:
            role = discord.utils.get(ctx.guild.roles, id=i[0])
            if i[1] > highest and role in ctx.author.roles:
                highest = i[1]

        raise NoPermission(f'You must have permission level `{permissionLevel}` to run this command! Your permission level is currently `{highest}`.')

    return commands.check(predicate)


def BotAdmin():
    async def predicate(ctx):
        result = fetch(f'SELECT * FROM PermissionOverride WHERE id = "{ctx.message.author.id}"')

        if result:
            if result[0][2] == 1:
                return result[0][2] == 1
            else:
                raise NoPermission('You must be a bot admin to run this command!')

        else:
            raise NoPermission('You must be a bot admin to run this command!')

    return commands.check(predicate)


def AccessCheck(ctx, permissionLevel: int = 10):
    result = fetch(f'SELECT * FROM PermissionOverride WHERE id = "{ctx.message.author.id}"')

    if result:
        return result[0][1] >= permissionLevel

    result2 = fetch(
        f'SELECT * FROM UserPermissions WHERE guildId = "{ctx.message.channel.guild.id}" AND id = "{ctx.message.author.id}"')

    if result2:
        return result2[0][1] >= permissionLevel

    result3 = fetch(
        f'SELECT * FROM RolePermissions WHERE guildId = "{ctx.message.channel.guild.id}" AND permissionLevel >= "{permissionLevel}"')

    for i in result3:
        role = discord.utils.get(ctx.guild.roles, id=i[0])
        if role in ctx.author.roles:
            return True

    return False


def BotAdminCheck(ctx):
    result = fetch(f'SELECT * FROM PermissionOverride WHERE id = "{ctx.message.author.id}"')

    if result:
        return result[0][2] == 1
    else:
        return False


def getPermissionLevel(user, guild):
    result = fetch(f'SELECT * FROM PermissionOverride WHERE id = "{user.id}"')

    if result:
        return result[0][1]

    result2 = fetch(f'SELECT * FROM UserPermissions WHERE guildId = "{guild.id}" AND id = "{user.id}"')

    if result2:
        return result2[0][1]

    result3 = fetch(f'SELECT * FROM RolePermissions WHERE guildId = "{guild.id}"')

    for i in result3:
        role = discord.utils.get(guild.roles, id=i[0])
        if i[1] > highest and role in user.roles:
            highest = i[1]

    return highest


def getBotAdmin(user):
    result = fetch(f'SELECT * FROM PermissionOverride WHERE id = "{user.id}"')

    if result:
        return True
    else:
        return False
