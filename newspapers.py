import re
import urllib.request
import time
import html
import os

commonUrl = 'http://gazeta-echo.ru/news/'

def download_page(pageUrl):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' 
    try:
        req = urllib.request.Request(pageUrl, headers = {'User-Agent': user_agent})
        with urllib.request.urlopen(req) as response:
            HTML = response.read().decode('utf-8')
    except:

        HTML = ""
    return HTML

def searching (HTML, pageUrl):
    
    row = '%s\t%s\t\t\t%s\t%s\tпублицистика\t\t\t%s\t\tнейтральный\tн-возраст\tн-уровень\tрайонная\t%s\tЭхо\t\t%s\tгазета\tРоссия\tКемеровская область\tru'
    if HTML != "":
        regPostHeader = re.compile ('<h2 class="section-title article-section-title">(.*?)      </h2>', flags=re.U | re.DOTALL)
        regPostAuthor = re.compile ('<p class="article-author">Автор: (.*?)</p>', flags=re.U | re.DOTALL)
        regPostCreated = re.compile ('<date class="article-date">([0-9]+?.*? 20[0-9][0-9]).*?</date>',  flags=re.U | re.DOTALL) #В принципе, можно и не искать, потому что месяц записан словом.
        regPostYear = re.compile ('<date class="article-date">[0-9]+?.*? (20[0-9][0-9]).*?</date>',  flags=re.U | re.DOTALL)
        regPostTopic = re.compile ('property="article:section" content="(.*?)" />',  flags=re.U | re.DOTALL)
        regPostText = re.compile ('<div class="entry-content">(.*?)<[ph]3? class=', flags=re.U | re.DOTALL)
        regPostMonth = re.compile ('<date class="article-date">[0-9]+? ([а-я]*?) 20[0-9][0-9].*?</date>',  flags=re.U | re.DOTALL)
        regPostDate = re.compile ('<date class="article-date">([0-9]+?) [а-я]*? 20[0-9][0-9].*?</date>',  flags=re.U | re.DOTALL)

        header = (html.unescape (''.join (regPostHeader.findall(HTML))))
        author = (html.unescape (''.join (regPostAuthor.findall (HTML))))
        if author == '':
            author = 'Noname' 
        topic = (html.unescape (''.join (regPostTopic.findall (HTML))))
        created = ''.join (regPostCreated.findall (HTML))
        year = ''.join (regPostYear.findall (HTML))
        month = ''.join (regPostMonth.findall (HTML))
        date = ''.join (regPostDate.findall (HTML))
        if month == "января":
            month_num = '1'
            month_num_0 = '01'
        if month == "февраля":
            month_num = '2'
            month_num_0 = '02'
        if month == "марта":
            month_num = '3'
            month_num_0 = '03'
        if month == "апреля":
            month_num = '4'
            month_num_0 = '04'
        if month == "мая":
            month_num = '5'
            month_num_0 = '05'
        if month == "июня":
            month_num = '6'
            month_num_0 = '06'
        if month == "июля": 
            month_num = '7' 
            month_num_0 = '07'
        if month == "августа":
            month_num = '8'
            month_num_0 = '08'
        if month == "сентября":
            month_num = '9'
            month_num_0 = '09'
        if month == "октября":
            month_num = '10'
            month_num_0 = '10'
        if month == "ноября":
            month_num = '11'
            month_num_0 = '11'
        if month == "декабря":
            month_num_0 = '12'
            month_num = '12'
        created_num = '%s.%s.%s' %(date, month_num_0, year)
        text = (html.unescape (''.join (regPostText.findall (HTML))))  
        cleaner_text = re.sub ('<.*?>', '', text)
        clean_text = re.sub (r'\\n', ' ', cleaner_text)      
           

        path = 'C:\\Users\\Tais\\YandexDisk\\газета\\plain\\%s\\%s' %(year, month_num)
        if not os.path.exists(path): 
            os.makedirs(path) 
        os.chdir(path) 
        file_name = "статья%d.txt" %I

        _f_ = open (file_name, 'w', encoding = 'utf-8')
        _f_.write (clean_text)
        _f_.close ()
        path_f = path + "\\" + file_name
        
        os.chdir ('C:\\Users\\Tais\\YandexDisk\\газета')
        f = open ('C:\\Users\\Tais\\YandexDisk\\газета\\metadata.csv', 'a', encoding = 'utf-8')
        row = '%s\t%s\t\t\t%s\t%s\tпублицистика\t\t\t%s\t\tнейтральный\tн-возраст\tн-уровень\tрайонная\t%s\t"Эхо"\t\t%s\tгазета\tРоссия\tКемеровская область\tru\n'
        f.write (row %(path_f, author, header, created_num, topic, pageUrl, year))
        f.close ()
        
        path2 = 'C:\\Users\\Tais\\YandexDisk\\газета\\mystem-xml\\%s\\%s' %(year, month_num)
        if not os.path.exists(path2): 
            os.makedirs(path2)
            
        path3 = 'C:\\Users\\Tais\\YandexDisk\\газета\\mystem-plain\\%s\\%s' %(year, month_num)
        if not os.path.exists(path3): 
            os.makedirs(path3)


        for i in range (5, 12): #Mystem почему-то не работает, даже из командной строки: выдаёт ошибку. Причину найти не могу.
        path = 'C:\\Users\\Tais\\YandexDisk\\газета\\plain\\2013\\' + str(i)
        path_2 = ' C:\\Users\\Tais\\YandexDisk\\газета\\mystem-xml\\2013\\' + str(i)
        path_3 = ' C:\\Users\\Tais\\YandexDisk\\газета\\mystem-plain\\2013\\' + str(i)
        lst = os.listdir(path)    
        for fl in lst:
                os.system(r"C:\Users\Tais\Desktop\mystem.exe " + path + os.sep + fl + path_2 + os.sep + fl + ' -cnid --format xml')
                os.system(r"C:\Users\Tais\Desktop\mystem.exe " + path + os.sep + fl + path_3 + os.sep + fl + ' -cnid --format xml')
            
        for i in range (1, 10):
        path = 'C:\\Users\\Tais\\YandexDisk\\газета\\plain\\2014\\' + str(i)
        path_2 = ' C:\\Users\\Tais\\YandexDisk\\газета\\mystem-xml\\2014\\' + str(i)
        path_3 = ' C:\\Users\\Tais\\YandexDisk\\газета\\mystem-plain\\2014\\' + str(i)
        lst = os.listdir(path)    
        for fl in lst:
                os.system(r"C:\Users\Tais\Desktop\mystem.exe " + path + os.sep + fl + path_2 + os.sep + fl + ' -cnid --format xml')
                os.system(r"C:\Users\Tais\Desktop\mystem.exe " + path + os.sep + fl + path_3 + os.sep + fl + ' -cnid --format xml')

#После разметки в Mystem:
        author, header, created_num, topic = adding (author, header, created_num, topic, pageUrl)
        ff = open (path_f, 'r', encoding = 'utf-8')
        text_ff = ff.read ()
        ff.close ()
        row2 = '@au %s\n@ti %s\n@da %s\n@topic %s\n@url %s\n' %(author, header, created_num, topic, pageUrl)
        text_full = row2 + text_ff
        ff = open (path_f, 'w', encoding = 'utf-8')
        ff.write (text_full)
        ff.close ()
        time.sleep(2)
        return 

def main():
       
    val1 = download_page (pageUrl)
    val2 = searching (val1, pageUrl)

if __name__ == '__main__' :
    os.makedirs ('C:\\Users\\Tais\\YandexDisk\\газета')
    f = open ('C:\\Users\\Tais\\YandexDisk\\газета\\metadata.csv', 'a', encoding = 'utf-8')
    f.write ('path\tauthor\tsex\tbirthday\theader\tcreated\tsphere\tgenre_fi\ttype\ttopic\tchronotop\tstyle\taudience_age\taudience_level\taudience_size\tsource\tpublication\tpublisher\tpubl_year\tmedium\tcountry\tregion\tlanguage\n')
    f.close ()
    I = 0

  

    
    for i in range (249, 1357): #Здесь так много разных ссылок, потому что иногда при обращении к статье открывалась заглавная страница какого-нибудь нового раздела, и программа падала.
        pageUrl = 'http://gazeta-echo.ru/news/' + str(i)
        if download_page(pageUrl) != "":
            I += 1
        main()
    for i in range (1368, 2133):
        pageUrl = 'http://gazeta-echo.ru/news/' + str(i)
        if download_page(pageUrl) != "":
            I += 1
        main()        
    for i in range (2145, 4104):
        pageUrl = 'http://gazeta-echo.ru/news/' + str(i)
        if download_page(pageUrl) != "":
            I += 1
        main()
    for i in range (4115, 13730):
        pageUrl = 'http://gazeta-echo.ru/news/' + str(i)
        if download_page(pageUrl) != "":
            I += 1
        main()

          

