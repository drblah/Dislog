import discord
import json

from logbarker import LogBarker

settings = json.load(open("settings.json", "r"))

print(settings)

log_barker = LogBarker(files=settings["files"], channelid=settings["channelid"])

log_barker.run(settings["api_key"])