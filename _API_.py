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

def vk_api(method, **kwargs):
    api_request = 'https://api.vk.com/method/'+method + '?'
    api_request += '&'.join(['{}={}'.format(key, kwargs[key]) for key in kwargs])
    return json.loads(requests.get(api_request).text)

group_info = vk_api('groups.getById', group_id='batrachospermum', v='5.63')
group_id = group_info['response'][0]['id']

posts = []
result = vk_api('wall.get', owner_id=-group_id, v='5.63', count=100)
posts += result["response"]["items"]

def _posts_ (posts):
    comments_count = []
    item_count = 200
    i = 1
    while len(posts) < item_count:
        result = vk_api('wall.get', owner_id=-group_id, v='5.63', count=100, offset=len(posts))
        posts += result['response']["items"]
        for post in posts:
        
            os.chdir (r"C:\Users\Tais\Desktop\Проект\Посты") 
            file_name_post = "пост%d.txt" %i
            _f_ = open (file_name_post, 'w', encoding = 'utf-8')
            _f_.write ((post["text"]).translate(non_bmp_map))
            _f_.close ()
            os.chdir (r"C:\Users\Tais\Desktop\Проект\Кол-во комментариев")
            num_of_comm = post["comments"]["count"]
            file_name_comment = "пост%d.txt" %i
            f = open (file_name_comment, 'w', encoding = 'utf-8')
            f.write (str(num_of_comm))
            f.close ()
            os.chdir (r"C:\Users\Tais\Desktop\Проект\Комментарии")
            file_name_comment = "пост%d.txt" %i
            f = open (file_name_comment, 'w', encoding = 'utf-8')
            f.write (str(post ["id"]))
            f.close ()
            i+=1

def _comments_():    
    comment_files = os.listdir(r"C:\Users\Tais\Desktop\Проект\Комментарии")
    d = {}
    for comment_file in comment_files:
        comments = []
        os.chdir (r"C:\Users\Tais\Desktop\Проект\Комментарии")
        f = open (comment_file, 'r', encoding = 'utf-8')
        post_id = f.read()
        f.close()
        resultC = vk_api('wall.getComments', owner_id=-group_id, post_id=post_id, v='5.63', count=100)
        comments += resultC["response"]["items"]
        
        item_count = 200
        if len(comments) > item_count:
            while len(comments) < item_count:
                result = vk_api('wall.getComments', owner_id=-group_id, post_id=post_id, v='5.63', count=100, offset=len(comments))
                comments += result['response']["items"]
                for comment in comments:
                    os.chdir (r"C:\Users\Tais\Desktop\Проект\Комментарии")
                    f = open (comment_file, 'a', encoding = 'utf-8')
                    f.write ((comment ["text"]).translate(non_bmp_map) + " ")
                    f.close ()
                    #os.chdir (r"C:\Users\Tais\Desktop\Проект\Комментаторы")
                    #f = open (comment_file, 'a', encoding = 'utf-8')
                    #f.write (str(comment ["from_id"]) + " ")
                    #f.close ()
                    #d[comment["from_id"]] = (comment ["text"]).translate(non_bmp_map)
                    if comment["from_id"] in d:

                        d[comment["from_id"]].append((comment ["text"]).translate(non_bmp_map))
                    else:
                        d[comment["from_id"]] = list()
                        d[comment["from_id"]].append((comment ["text"]).translate(non_bmp_map))
        else:
            result = vk_api('wall.getComments', owner_id=-group_id, post_id=post_id, v='5.63', count=100, offset=len(comments))
            comments += result['response']["items"]
            for comment in comments:
                os.chdir (r"C:\Users\Tais\Desktop\Проект\Комментарии")
                f = open (comment_file, 'a', encoding = 'utf-8')
                f.write ((comment ["text"]).translate(non_bmp_map) + " ")
                f.close ()
                #os.chdir (r"C:\Users\Tais\Desktop\Проект\Комментаторы")
                #f = open (comment_file, 'a', encoding = 'utf-8')
                #f.write (str(comment ["from_id"]) + " ")
                #f.close ()
                #d[comment["from_id"]] = len((((comment ["text"]).translate(non_bmp_map).replace('— ', '')).replace('- ', '')).split())
                if comment["from_id"] in d:                   
                    d[comment["from_id"]].append(len((((comment ["text"]).translate(non_bmp_map).replace('— ', '')).replace('- ', '')).split()))
                else:
                    d[comment["from_id"]] = []
                    d[comment["from_id"]].append(len((((comment ["text"]).translate(non_bmp_map).replace('— ', '')).replace('- ', '')).split()))
    d1 = {}
    d2 = {}
    d3 = {}
    d4 = {}
    d5 = {}
    for user in d:
        num_of_com = len(d[user])
        summ = 0
        for number in d[user]:
            summ += int(number)
            av_comm = int(summ)/num_of_com
            d1[user] = av_comm
        result = vk_api('users.get', user_ids=user, fields="city, bdate", v='5.63')
        if result ["response"]:
            if 'bdate' in result["response"][0]:
                age = result["response"][0]["bdate"]
                year = re.search ('\.([0-9]{4})', age)
                if year:
                    year = year.group(1)
                    month = re.search ('[0-9]{1,2}\.([0-9]{1,2})\.([0-9]{4})', age)
                    month = month.group(1)
                    day = re.search ('([0-9]{1,2})\.[0-9]{1,2}\.([0-9]{4})', age)
                    day = day.group(1)
                    today = date.today()
                    age_ = today.year - int(year)
                    if today.month < int(month):
                        age_ -= 1
                    elif today.month == int(month) and today.day < int(day):
                        age_ -= 1
                    age = age_
                    
                    if age in d2:
                        d2[age].append(d1[user])
                    else:
                        d2[age] = []
                        d2[age].append(d1[user])
                else:
                    #age = "no_age"
                    #if age in d2:
                    #    d2[age].append(d1[user])
                    #else:
                     #   d2[age] = []
                      #  d2[age].append(d1[user])
                    continue
            else:
                #age = "no_age"
                #if age in d2:
                #    d2[age].append(d1[user])
                #else:
                   # d2[age] = []
                   # d2[age].append(d1[user])   
                    continue
        else:
            continue
        summ = 0        
        for number in d2[age]:
            num_of_com = len(d2[age])
            summ += int(number)
            av_comm = int(summ)/num_of_com
            d3[age] = av_comm                
                
        if 'city' in result["response"][0]:
            city = result["response"][0]["city"]["title"]
            if city in d4:
                d4[city].append(d1[user])
            else:
                d4[city] = []
                d4[city].append(d1[user])
        else:
               # city = "no_city"
                #if city in d4:
                #    d4[city].append(d1[user])
                #else:
                 #   d4[city] = []
                 #   d4[city].append(d1[user])
                continue
        summ = 0        
        for number in d4[city]:
            num_of_com = len(d4[city])
            summ += int(number)
            av_comm = int(summ)/num_of_com
            d5[city] = av_comm
    X = list(d3.keys())
    Y = list (d3.values())
    plt.bar(X, Y)
    plt.title("Соотношение возраста со средней длиной комментария", fontsize=10)
    plt.xlabel("Возраст (в годах)", fontsize=10)
    plt.ylabel("Средняя длина комментария (в словах)", fontsize=10)
    os.chdir (r"C:\Users\Tais\Desktop\Проект")
    plt.savefig('age_&_com_len.png')
    plt.show()
    city_labels = sorted(d5.keys())
    city = [i for i in range(len(city_labels))]
    comm_len = [d5[key] for key in city_labels]
    plt.bar(city, comm_len, color = 'c')
    plt.xticks(city, city_labels, rotation='vertical')
    plt.title("Соотношение города комментатора со средней длиной комментария", fontsize=10)
    plt.xlabel("Город", fontsize=10)
    plt.ylabel("Средняя длина комментария (в словах)", fontsize=10)
    os.chdir (r"C:\Users\Tais\Desktop\Проект")
    plt.savefig('city_&_com_len.png')
    plt.show()

def _len_post_ ():
    len_posts = []
    #i = 1   
    post_files = os.listdir(r"C:\Users\Tais\Desktop\Проект\Посты")
    for post_file in post_files:
        os.chdir (r"C:\Users\Tais\Desktop\Проект\Посты") 
        f = open (post_file, 'r', encoding = 'utf-8')
        post = f.read()
        f.close()
        post = post.split ()
        len_post = len (post)
        os.chdir (r"C:\Users\Tais\Desktop\Проект\Посты_длина") 
        #file_name_post = "пост%d.txt" %i
        file_name_post = post_file
        _f_ = open (file_name_post, 'w', encoding = 'utf-8')
        _f_.write (str(len_post))
        _f_.close ()
        #i += 1
        len_posts.append (len_post)
    return len_posts

def _len_comments_ ():
    len_comments = []
    
    comment_files = os.listdir(r"C:\Users\Tais\Desktop\Проект\Комментарии")
    comments_count_f = os.listdir(r"C:\Users\Tais\Desktop\Проект\Кол-во комментариев")
    
    for comment_info in zip (comment_files, comments_count_f): 
        comment_file = comment_info[0]
        os.chdir (r"C:\Users\Tais\Desktop\Проект\Комментарии") 
        f = open (comment_file, 'r', encoding = 'utf-8')
        comment = f.read()
        f.close()
        comment = comment.replace('— ', '')
        comment = comment.replace('- ', '')
        comment = comment.split ()
        comments_count_f = comment_info[1]
        os.chdir (r"C:\Users\Tais\Desktop\Проект\Кол-во комментариев") 
        f = open (comment_file, 'r', encoding = 'utf-8')
        comment_count = f.read()
        f.close()
        if int(comment_count) == 0:
            len_comment = 0
            len_comments.append (len_comment)
        else:
            len_comment = round(len (comment)/int(comment_count))
            len_comments.append (len_comment)
    return len_comments

def _graph_ ():
    X = _len_post_()
    Y = _len_comments_()
    #plt.plot(X, Y, color = 'y')
    #plt.scatter(X, Y, color = 'y') 
    plt.bar(X, Y, color = 'g')
    plt.title("Соотношение длины поста со средней длиной комментария", fontsize=10)
    plt.xlabel("Длина поста (в словах)", fontsize=10)
    plt.ylabel("Средняя длина комментария (в словах)", fontsize=10)
    os.chdir (r"C:\Users\Tais\Desktop\Проект")
    plt.savefig('post_len_&_com_len.png')
    plt.show()


def main ():
    val_1 = _posts_(posts)
    val_2 = _comments_()
    val_5 = _graph_()
    

if __name__ == '__main__' :
    main()
