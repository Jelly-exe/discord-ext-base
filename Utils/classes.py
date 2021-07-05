from discord.ext import commands


class Command(commands.Command):
    def __init__(self, *args, **kwargs):
        self.access = kwargs.pop('access')
        super().__init__(*args, **kwargs)


class Group(commands.Group):
    def __init__(self, *args, **kwargs):
        self.access = kwargs.pop('access')
        super().__init__(*args, **kwargs)

