import flask
import telebot
import conf
import random
import re
from pymorphy2 import MorphAnalyzer

#WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
#WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

#bot = telebot.TeleBot(conf.TOKEN, threaded=False)

#bot.remove_webhook()
#bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

#app = flask.Flask(__name__)

#@bot.message_handler(commands = ['start', 'help'])
#def send_welcome (message):
#	bot.send_message (message.chat.id, "Привет! :)")
	
def _lexicon_ ():
        lex = []
        d = {}
        morph = MorphAnalyzer()
        f = open ('Text.txt', 'r', encoding = 'utf-8')
        words = (((f.read()).replace('— ', '')).replace('– ', '')).split()
        f.close()
        for word in words:
                word = (word.strip(".,!?\-[]:»«")).lower()
                ana = (morph.parse(word))[0]
                lemma = ana.normalized
                if 'UNKN' not in lemma.tag:
                        #if ' ' in str(lemma.tag):
                        #       lemma_change = (str(lemma.tag)).split(' ')[1]
                        lemma_const = (str(lemma.tag)).split(' ')[0]
                        d[lemma] = [lemma_const]
        return (d)

message = input ("Напиши мне что-нибудь! ")
print ("Подожди, я придумываю ответ пооригинальнее...")

#@bot.message_handler (func=lambda m: True)
def _reply_ (message):
        morph = MorphAnalyzer()
        reply = ''
        #message_words = message.text.split()
        d = _lexicon_()
        message_words = message.split()
        
        for word in message_words:
                w = ''
                a = []
                A = []
                word = (word.strip(".,!?\-[]:»«“„")).lower()
                ana = (morph.parse(word))[0]
                form = ana.tag
                nach_form = ana.normalized
                nach_form_form = nach_form.tag
                for lemma in d:
                        if (str(nach_form_form)).split(' ')[0] == d[lemma][0]:
                            if lemma.word not in a:
                                a.append(lemma.word)
                w = random.choice (a)
                if len((str(form)).split(' ')) == 2:
                    for element in (((morph.parse(w))[0])).lexeme:
                        if re.findall(((str(form))),(str(element.tag))):
                            if element.word not in A:
                                A.append (element.word)                   
                                w = random.choice (A)
                reply += w + ' '        
        reply = reply [:-1]                        
        print (reply.capitalize() + '.')
        #bot.send_message(message.chat.id, reply)
_reply_ (message)

#@app.route ('/', methods=['GET', 'HEAD'])
#def index ():
#    return 'ok'

 
#if __name__ == '__main__':
#    bot.polling(none_stop=True)

#@app.route (WEBHOOK_URL_PATH, methods=['POST'])
#def webhook ():
#    if flask.request.headers.get('content-type') == 'application/json':
#        json_string = flask.request.get_data().decode('utf-8')
#        update = telebot.types.Update.de_json(json_string)
#        bot.process_new_updates([update])
#        return ''
#    else:
#        flask.abort(403)
        
