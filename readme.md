# delugebot

Telegram bot for interacting with [Deluge](https://deluge-torrent.org/) torrent client. Currently supports adding new downloads with torrent magnet link.

## Installation

Clone the repository to your server where you intend to host this bot

```bash
git clone https://github.com/v3se/delugebot
```

Build the image with

```bash
docker build -t <tag> .
```

Enable WebAPI in your Deluge client. Check [this](https://pypi.org/project/deluge-webapi/) link for installation instructions.

Create a new [Telegram bot](https://core.telegram.org/bots#6-botfather) if you haven't created one yet and retrieve the chat id. To do that you can run the docker only with the TELEGRAM_TOKEN environment variable

```bash
docker run -e TELEGRAM_TOKEN=<telegram-bot-token> <container>
```

After this you can issue the _/start_ command to the bot. The bot will log the chat id to the container stdout. You can check it with this command

```bash
docker logs <container>
...
"Chat ID not in allowed ids: xxxxxxxx"
```

## Usage

```bash
docker run --name delugebot \
-e ALLOWED_IDS=<allowed-chat-ids>  \
-e DELUGE_ADDRESS=<ip-addr> \
-e WEPAPI_PASSWD=<passwd> \
-e TELEGRAM_TOKEN=<telegram-bot-token> <container>
```

After starting the container you will need to issue the _/start_ command to the bot to initialize it.

To add a new torrent from a magnet link, use the _/magnet_ command and add the link after the command in the same message

### Arguments

**ALLOWED_IDS**

This argument defines which Telegram chat ids can use this bot. Mainly for security purposes so anyone else can't use your bot

**DELUGE_ADDRESS**

Address to the Deluge WebUI. The default will be _127.0.0.1:8112_

**WEBAPI_PASSWD**

Password for the Deluge WebUI

**TELEGRAM_TOKEN**

Telegram bot token which you received when creating the bot
