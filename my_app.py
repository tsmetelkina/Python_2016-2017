import flask
import telebot
import conf

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)  

bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

@bot.message_handler(commands = ['start', 'help'])
def send_welcome (message):
	bot.send_message (message.chat.id, "Привет! Я посчитаю, сколько слов в твоём сообщении. Отправь мне что-нибудь ;)")

@bot.message_handler (func=lambda m: True)
def send_len (message):
        if len(message.text.split()) <= 3:
                bot.send_message(message.chat.id, 'Слов в твоём сообщении: {}. Краткость — сестра таланта :)'.format(len(message.text.split())))
        elif len (message.text.split()) >= 15:
                bot.send_message(message.chat.id, 'Слов в твоём сообщении: {}. У тебя в роду никого с фамилией Толстой не было?.. :)'.format(len(message.text.split())))
        else:
                bot.send_message(message.chat.id, 'Слов в твоём сообщении: {}.'.format(len(message.text.split())))
                
@app.route ('/', methods=['GET', 'HEAD'])
def index ():
    return 'ok'
 
@app.route (WEBHOOK_URL_PATH, methods=['POST'])
def webhook ():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
        
