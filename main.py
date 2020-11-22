import requests
import logging
import json
from telegram.ext import Updater
from telegram.ext import CommandHandler
from os import environ

logging.basicConfig(format='%(asctime)s %(message)s',level="INFO", datefmt='%d/%m/%Y %H:%M:%S')

WEBAPI_PASSWD = environ.get('WEBAPI_PASSWD')
TELEGRAM_TOKEN = environ.get('TELEGRAM_TOKEN')
DELUGE_ADDRESS = environ.get('DELUGE_ADDRESS', '127.0.0.1:8112')
COOKIES = None
ALLOWED_IDS = json.loads(environ.get('ALLOWED_IDS'))
REQUEST_ID = 0

updater = Updater(token=TELEGRAM_TOKEN)
dispatcher = updater.dispatcher

mybots = {}

def start(bot, update):
    """Send a message when the command /start is issued."""
    chat_id = update.message.chat_id
    logging.info("Received start command from chat id: {}".format(chat_id))
    if chat_id in ALLOWED_IDS:
        mybots[chat_id] = bot
        update.message.reply_text("Deluge Bot Started Successfully")
    else:
        logging.error("Chat ID not in allowed ids: {}".format(chat_id))

def send_later(msg):
    for id, bot in mybots.items():
        bot.send_message(id, text=msg)

def send_request_deluge(method, params=None):
    global REQUEST_ID
    global COOKIES
    REQUEST_ID += 1

    try:

        response = requests.post(
            'http://{}/json'.format(DELUGE_ADDRESS),
            json={'id': REQUEST_ID, 'method': method, 'params': params or []},
            cookies=COOKIES)

    except requests.exceptions.ConnectionError:
        raise Exception('WebUI seems to be unavailable')

    data = response.json()

    error = data.get('error')

    if error:
        msg = error['message']

        if msg == 'Unknown method':
            msg += '. Check WebAPI is enabled.'

        raise Exception('API response: %s' % msg)
        send_later(msg)

    COOKIES = response.cookies

    return data['result']

def add_magnet(bot, update):
    if update.message.chat_id not in mybots:
        logging.error("Chat ID not in allowed ids: {}".format(update.message.chat_id))
        return 0
    magnet_link = update.message.text.split(" ")[1]
    send_request_deluge('auth.login', [WEBAPI_PASSWD])
    r = send_request_deluge('webapi.add_torrent', [magnet_link])
    if not r:
        logging.info("Invalid magnet link: {}".format(magnet_link))
        send_later("Invalid torrent. Check magnet URI")
    else:
        send_later("Torrent added")
        logging.info("Magnet link added: {}".format(magnet_link))

def main():
    logging.info("Deluge bot started!")
    logging.info("Deluge WebAPI Address: {}".format(DELUGE_ADDRESS))
    start_handler = CommandHandler('start', start)
    magnet_handler = CommandHandler('magnet', add_magnet)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(magnet_handler)
    updater.start_polling()
    logging.info("Listening commands")
    
if __name__ == '__main__':
    main()
