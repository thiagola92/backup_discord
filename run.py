import os
from pathlib import Path
from urllib.parse import urlparse

import requests
from discord import Client, Intents

intents = Intents.default()
intents.message_content = True

client = Client(intents=intents)


@client.event
async def on_ready():
    print("STARTED")


@client.event
async def on_message(message):
    if not message.content.startswith("$backup") or message.author.bot:
        return

    print(f"CHANNEL >> {message.channel}")

    async for m in message.channel.history(limit=None):
        if m.id == message.id:
            continue

        if m.author == message.author:
            download_content(m.content)

    print("END")


def download_content(url, suffix=".gif"):
    if not is_url_valid(url):
        return

    path = urlparse(url).path
    name = Path(path).name

    if not Path(path).suffix:
        return download_content(url + suffix)

    if Path(f"backup/{name}").exists():
        return

    print(url)

    response = requests.get(url)
    with open(f"backup/{name}", "wb") as file:
        file.write(response.content)


def is_url_valid(url):
    result = urlparse(url)

    try:
        return all([result.scheme, result.netloc])
    except:
        return False


client.run(os.environ["TOKEN"])
