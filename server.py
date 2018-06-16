from flask import Flask, request
from slugbot import botutils
import configs
import utils
import threading

app = Flask(__name__)
context = configs.SSL_CONTEXT

bot = botutils.SlugBot(configs.ACCESS_TOKEN)
easter_slug = utils.EasterEggHandler(bot)
chatting_slug = utils.ChatHandler(bot)




@app.route('/', methods=['POST'])
def handle_incoming_messages():
    #Information
    data = request.json
    userid = data['entry'][0]['messaging'][0]['sender']['id']
    timestamp = data['entry'][0]['messaging'][0]['timestamp']
    msg = ''
    if 'text' in data['entry'][0]['messaging'][0]['message']:
        msg = data['entry'][0]['messaging'][0]['message']['text']
    #/Information
    user = botutils.User(userid, 0)
    utils.localize(user)

    if msg.startswith('/'):
        command_task = threading.Thread(target=bot.runCommand, name='command_task', args=(user, msg))
        command_task.start()

    else:
        if easter_slug.on_message(user, msg) == 0:
            chatting_slug.on_message(user, msg)

    return 'ok'


@app.route('/', methods=['GET'])
def handle_verification():
    if 'hub.verify_token' in request.args:
        if request.args['hub.verify_token'] == configs.VERIFY_TOKEN:
            return request.args['hub.challenge']
    return 'Invalid token'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=configs.PORT, debug=True, ssl_context=context)