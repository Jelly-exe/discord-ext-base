import json

from discord.ext.base.Utils.nestedDict import DynamicAccessNestedDict


def config(runType, filename):
    with open(f'Configs/Production/{filename}', encoding='utf8') as file:
        configFile = DynamicAccessNestedDict(json.load(file))

    if runType == "development":
        with open(f'Configs/Development/{filename}', encoding='utf8') as file:
            devConfig = json.load(file)

        for key, value in devConfig.items():
            configFile.setval(key, value)

    return configFile.data
