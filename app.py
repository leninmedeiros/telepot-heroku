import os
from flask import Flask, request
import telepot
import time

try:
    from Queue import Queue
except ImportError:
    from queue import Queue

app = Flask(__name__)
# put your token in heroku app as environment variable
TOKEN = os.environ['PP_BOT_TOKEN']
SECRET = '/bot' + TOKEN
# paste the url of your application
URL = 'https://telepot-heroku.herokuapp.com'

UPDATE_QUEUE = Queue()
BOT = telepot.Bot(TOKEN)


def on_chat_message(msg):
    print("I guess I'm listenning...")
    content_type, chat_type, chat_id = telepot.glance(msg)
    BOT.sendMessage(chat_id, 'hello!')

# take updates from queue
BOT.message_loop({'chat': on_chat_message}, source=UPDATE_QUEUE)


@app.route(SECRET, methods=['GET', 'POST'])
def pass_update():
    UPDATE_QUEUE.put(request.data)  # pass update to bot
    return 'OK'

time.sleep(5)
BOT.setWebhook(URL + SECRET)
time.sleep(5)
