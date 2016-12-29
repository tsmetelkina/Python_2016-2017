import re
import urllib.request
import os

pageUrl = 'http://web-corpora.net/Test2_2016/short_story.html'

def first_and_second(pageUrl):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' 
    try:
        req = urllib.request.Request(pageUrl, headers = {'User-Agent': user_agent})
        with urllib.request.urlopen(req) as response:
            HTML = response.read().decode('utf-8')
    except:
        HTML = ""
    print ('\nПервое задание:\n')
    if HTML != "":
        regWords = re.compile ('[А-Яа-яё-]+', flags=re.U | re.DOTALL)
        words = regWords.findall (HTML)
        for word in words:
            wordWithC = re.findall('^[сС]', word)
            if wordWithC:
                print (word)
                f = open ('input.txt', 'a', encoding = 'utf-8')
                word = word.split('-')[0] #Это нужно потому, что Mystem размечает слова, написанные через дефис (типа "синие-синие"), как 2 слова, и таблица SQL съезжает. Можно было изначально считать такие слова двумя разными, но я об этом слишком поздно подумала и не успела исправить :)
                f.write (word + '\n')
                f.close ()
                
    print ('\nВторое задание:\n')
    os.system ('mystem.exe input.txt output.txt -nigd')
    f2 = open ('output.txt', 'r', encoding = 'utf-8')
    words = f2.readlines()
    f2.close()
    for word in words:
        verbs = re.findall ('=V', word)
        if verbs:
            print (word.split ('{')[0])
    return

def third ():
    f = open ('input.txt', 'r', encoding = 'utf-8')
    tokens = f.readlines()
    f.close()
    f2 = open ('output.txt', 'r', encoding = 'utf-8')
    lemmas_and_pos = f2.readlines()
    f2.close()
    i = 0
    for element, token in zip (lemmas_and_pos, tokens):
        i += 1
        token = token.split('\n')[0]
        lemma = (((element.split ('{')[1]).split ('='))[0]).strip ('?')
        pos = (re.search ('[A-Z]+', element)).group(0)
        string = 'INSERT INTO the_Table (id, lemma, token, part_of_speech) VALUES ("%d", "%s", "%s", "%s");\n' %(i, lemma, token, pos)
        #string = 'INSERT INTO the_Table (id, лемма, словоформа, часть речи) VALUES ("%d", "%s", "%s", "%s");\n' %(i, lemma, token, pos) Если всё-таки принципиально, чтобы столбцы назывались точно так, как это указано в задании.
        f3 = open ('inserts.txt', 'a', encoding = 'utf-8')
        f3.write (string)
        f3.close()
        
def main():
       
    val1 = first_and_second (pageUrl)
    val2 = third ()

if __name__ == '__main__' :
    main()
