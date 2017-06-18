"""
Веб-приложение: обратиться через API VK к заданному набору сообществ,
скачать записи за определённый период
и построить графики частотности ключевых для тематки сообщества слов
для сообществ, посвящённым фильмам, "режиссёр", "кино", "премьера", "показ", "блокбастер",
остальные найти через семантические вектора)
"""
import requests
import os
import json
import re
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
from datetime import date
import sys
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

import warnings
warnings.filterwarnings (action = 'ignore', category=UserWarning, module='gensim')

import gensim
import re
from pymystem3 import Mystem

import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')


def vk_api(method, **kwargs):
    api_request = 'https://api.vk.com/method/'+method + '?'
    api_request += '&'.join(['{}={}'.format(key, kwargs[key]) for key in kwargs])
    return json.loads(requests.get(api_request).text)


def _posts_ (group_id, posts):
    comments_count = []
    item_count = 1550 #Это максимальное число записей, которое можно было выложить с 1 по 31 мая.
    i = 1
    while len(posts) < item_count:
        result = vk_api('wall.get', owner_id=-group_id, v='5.63', count=100, offset=len(posts))
        posts += result['response']["items"]
        print (len(posts))
        
    for post in posts:
        date = post["date"]
        if date in range (1493586000, 1496264399): #Unix. C 01.05.2017, 0:00:00 по 31.05.2017, 23:59:59 (Мск)
            os.chdir (r"C:\Users\Tais\Desktop\Проек\Posts\%s" %group_id) 
            file_name_post = "post_%s_%d.txt" %(group_id, i)
            _f_ = open (file_name_post, 'w', encoding = 'utf-8')
            _f_.write ((post["text"]).translate(non_bmp_map))
            _f_.close ()
            i += 1
            
def _vectors_():
    m = 'ruwikiruscorpora_0_300_20.bin'
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
    model.init_sims(replace=True)

    words = ['режиссер_NOUN', 'кино_NOUN', 'премьера_NOUN', 'показ_NOUN', 'блокбастер_NOUN'] 
    a = []
    for word in words:
        if word in model:
            if word.split("_")[0] not in a:
                a.append ((word.split("_"))[0])
                for i in model.most_similar(positive=[word], topn=10):
                    if i[0].split("_")[0] not in a:
                        a.append(((i[0]).split("_")[0]).replace ('::', ' '))
        else:
            print(word + ' is not present in the model')
    print (a)
    return a

def _graph_1_(d):
    word_labels = sorted(d.keys())
    word = [i for i in range(len(word_labels))]
    stats = [d[key] for key in word_labels]
    plt.bar(word, stats, color = 'palevioletred')
    plt.xticks(word, word_labels, rotation='vertical')
    plt.title("Число употреблений ключевых слов", fontsize=10)
    plt.xlabel("Слово", fontsize=10)
    plt.ylabel("Число употреблений слова", fontsize=10)
    os.chdir (r"C:\Users\Tais\Desktop\Проек")
    plt.savefig('n_gr_1.png')
    plt.show()
    
def _graph_2_(d):
    word_labels = sorted(d.keys())
    word = [i for i in range(len(word_labels))]
    stats = [d[key] for key in word_labels]
    plt.bar(word, stats, color = 'pink')
    plt.xticks(word, word_labels, rotation='vertical')
    plt.title("Частотность ключевых слов", fontsize=10)
    plt.xlabel("Слово", fontsize=10)
    plt.ylabel("Частота встрчаемости слова в %", fontsize=10)
    os.chdir (r"C:\Users\Tais\Desktop\Проек")
    plt.savefig('n_gr_2.png')
    plt.show()
    
def _statistics_ ():
    len_posts = 0
    d = {}
    m = Mystem()
    os.chdir (r'C:\Users\Tais\Desktop\Проек')    
    f3 = open ('ALLPOSTS.txt', 'r', encoding = 'utf-8')
    post = f3.read()
    f3.close()
    lemmas = m.lemmatize(post)   
    lemmas = ''.join(lemmas)
    f4 = open ('lemmaposts.txt', 'a', encoding = 'utf-8')
    f4.write(lemmas) 
    f4.close()
    for word in _vectors_():
        w = re.findall (word, post)
        if w:
            i = len (w)
            if word in d:
                d[w[0]] += i
            else:
                d[w[0]] = i
          
    # Майстем считает GenPl слова "премьера" словом "премьер", поэтому вручную подправим наш словарь.
    d = {'премьера': 27, 'дебют': 2, 'телевидение': 7, 'актер': 31, 'триллер': 13, 'показ': 23, 'продюсер': 3, 'экранизация': 3, 'сценарист': 8, 'кино': 99, 'постановщик': 7, 'режиссер': 57, 'кинематографист': 3, 'релиз': 7, 'кинопроект': 2, 'кинематограф': 4, 'фильм': 182}

    _graph_1_(d)    
    post_l = post.split ()
    len_posts = len (post_l)     
    for word in d:
        stats = (d[word] / len_posts) * 100
        d[word] = stats        
    _graph_2_(d)    
    return (d)
            
def main ():
    group_urls = ['hofilm', 'xfilm', 'public.cinemaholics', 'kinopoisk', 'drugoekino']
    for group_url in group_urls:
        group_info = vk_api('groups.getById', group_id=group_url, v='5.63')
        group_id = group_info['response'][0]['id']
        posts = []
        result = vk_api('wall.get', owner_id=-group_id, v='5.63', count=100)
        posts += result["response"]["items"] 
        val_1 = _posts_(group_id, posts)
        
    _statistics_()

if __name__ == '__main__' :
    main()

