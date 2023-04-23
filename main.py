from discord.ext.base import bot

client = bot.BaseBot(True, ['test', 'test'])
client.run(client.getToken())
