import json
import logging
import os
import sys
from typing import Tuple

import discord
from discord import app_commands
from discord.app_commands import AppCommandError
from discord.ext import commands
from datetime import datetime

from .database import Database
from .logger import Logger
from .config import config


class BaseBot(commands.Bot):

    @property
    def config(self):
        return self._config

    @property
    def secure(self):
        return self._secure

    def __init__(self, devMode: bool, status: Tuple[str, str]):
        self.databaseURI = None
        self.step = 0
        self.persistent_views_added = False

        self.runType = "production"
        loggerFormat = "[%DATE% | %TIME%] [%TAG%] %MSG%"
        self.logger = Logger(loggerFormat, False)

        self.devMode = devMode
        if devMode:
            self.logger = Logger(loggerFormat, True)
            self.runType = "development"

        self.logger.startup(f'{self._displayStep()}. Reading configs\'s')
        self._config = self.get_config()
        self._secure = self.get_secure()

        self.logger.startup(f'{self._displayStep()}. Defining extensions and guild object')
        self.initial_extensions = []
        self.botGuild = discord.Object(id=self.config["guildId"])

        self.logger.startup(f'{self._displayStep()}. Setting activity')
        activity = discord.Activity(name=status[1] if devMode else status[0], type=discord.ActivityType.playing)

        self.logger.startup(f'{self._displayStep()}. Setting up intents')
        intents = discord.Intents.all()
        intents.members = True
        intents.guilds = True
        intents.presences = True
        intents.message_content = True

        self.logger.startup(f'{self._displayStep()}. Connecting to database')
        self.database = self.get_database()

        self.logger.startup(f'{self._displayStep()}. Initializing the bot')
        super().__init__(command_prefix=self._getPrefix(),
                         help_command=None,
                         owner_id=278548721778688010,
                         activity=activity,
                         intents=intents,
                         case_insensitive=True)

        self.logger.startup(f'{self._displayStep()}. Setting the boot time')
        self.boot = datetime.now()

        self.logger.startup(f'{self._displayStep()}. Setting the token')
        self.token = self.secure[self.runType]["token"]

        self.tree.error(self.on_slash_command_error)

        self.matchIds = []
        self.extra()

    def extra(self):
        pass

    def get_config(self):
        return config(self.runType, "config.json")

    def get_secure(self):
        return config("production", "secure.json")

    def get_database(self) -> Database:
        return None

    async def _getCogs(self):
        dontLoad = []
        for i in os.listdir('Cogs'):
            if i.endswith('.py') and i not in dontLoad:
                self.initial_extensions.append(f'Cogs.{i[:-3]}')

    async def ReloadCogs(self):
        await self._getCogs()
        for ext in self.initial_extensions:
            try:
                await self.unload_extension(ext)
                await self.load_extension(ext)
                self.logger.startup(f'{self._displayStep()}. Reloading {ext}')
            except Exception as error:
                self.logger.critical(f'{self._displayStep()}. {ext} cannot be loaded. [{error}]')

    async def loadCogs(self):
        await self._getCogs()
        for ext in self.initial_extensions:
            try:
                await self.load_extension(ext)
                self.logger.startup(f'{self._displayStep()}. Loading {ext}')
            except Exception as error:
                self.logger.critical(f'{self._displayStep()}. {ext} cannot be loaded. [{error}]')

    async def setup_hook(self):
        await self.loadCogs()

    def _displayStep(self) -> int:
        self.step += 1
        return self.step

    async def on_ready(self):
        self.logger.startup(f'~~~~~~~~~~~~~')
        self.logger.startup(f'Logged in as - ')
        self.logger.startup(f'Name: {self.user.name}')
        self.logger.startup(f'Id: {self.user.id}')
        self.logger.startup(f'Time: {self.boot}')
        self.logger.startup(f'~~~~~~~~~~~~~')
        self.logger.startup(f'(Pterodactyl Bot Online)')

        if self.devMode:
            self.logger.startup(f'DEV MODE')

        self.tree.copy_global_to(guild=self.botGuild)
        self.tree.clear_commands(guild=None)
        await self.tree.sync(guild=self.botGuild)

    @staticmethod
    async def on_slash_command_error(interaction: discord.Interaction, error: AppCommandError):
        if isinstance(error, app_commands.CheckFailure):
            pass
        else:
            embed = discord.Embed(
                description=f'{error.args[0]}\n\nPlease alert the developers of this error.',
                color=discord.Colour.from_str(interaction.client.config['embed']['colour'])
            )
            try:
                await interaction.response.send_message(embed=embed, ephemeral=True)
            except:
                try:
                    await interaction.followup.send(embed=embed, ephemeral=True)
                except:
                    await interaction.channel.send(embed=embed)

            _log = logging.getLogger(__name__)
            _log.error(error)

            _log = logging.getLogger(__name__)
            _log.error(error)

    async def ReloadConfig(self):
        self.config = config(self.runType, "config.json")

    def _getPrefix(self) -> str:
        return self.config["prefix"]

    def getToken(self) -> str:
        return self.token
