import discord

from datetime import datetime
from . import colours


class Logger:
    def __init__(self, client, log_format: str, debug: bool):
        self.client = client
        self.format: str = log_format
        self.debug: bool = debug

    def buildFormat(self, tag: str, colour: str, msg: str) -> str:
        return colour + self.format.replace("%DATE%", datetime.now().strftime("%d %m %Y")).replace("%TIME%", datetime.now().strftime("%H:%M:%S")).replace("%TAG%", tag).replace("%MSG%", msg)

    def info(self, msg: str) -> None:
        print(self.buildFormat("INFO", colours.OKCYAN, msg))

    def debug(self, msg: str) -> None:
        if self.debug:
            print(self.buildFormat("DEBUG", colours.OKCYAN, msg))

    def warn(self, msg: str) -> None:
        print(self.buildFormat("WARNING", colours.WARNING, msg))

    def error(self, msg: str) -> None:
        print(self.buildFormat("ERROR", colours.FAIL, msg))

    def critical(self, msg: str) -> None:
        print(self.buildFormat("CRITICAL", colours.FAIL, msg))

    def success(self, msg: str) -> None:
        print(self.buildFormat("SUCCESS", colours.OKGREEN, msg))

    def console(self, msg: str) -> None:
        print(self.buildFormat("CONSOLE", colours.OKBLUE, msg))

    def command(self, command: str, author: discord.Member) -> None:
        print(self.buildFormat("INFO", colours.OKCYAN, f'{author.display_name} issued command {command}'))

    def startup(self, msg: str) -> None:
        print(self.buildFormat("STARTUP", colours.OKBLUE, msg))
