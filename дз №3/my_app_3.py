import re
import urllib.request
import html

URL = ["http://tass.ru/kultura/3834041", "https://rg.ru/2016/12/02/video-kristen-stiuart-vstrechaet-zebru-v-novom-klipe-rolling-stones.html", "http://www.wonderzine.com/wonderzine/entertainment/entertainment-news/222807-ride-em-on-down", "http://www.rosbalt.ru/style/2016/12/02/1572409.html"]

def download_search_set_write(URL):
    i = 1
    for element in URL:
        pageUrl = element
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' 

        req = urllib.request.Request(pageUrl, headers = {'User-Agent': user_agent})
        with urllib.request.urlopen(req) as response:
            HTML = response.read().decode('utf-8')        
            
            regPostText = re.compile('<p>(.*?)</p>', flags=re.U | re.DOTALL)
            textStr = html.unescape(''.join(regPostText.findall(HTML)))
            regCleaning = re.compile('<.*?>', flags=re.U | re.DOTALL)
            c_text = regCleaning.sub (" ", textStr)
            regCleaning2 = re.compile('/.*?/. ', flags=re.U | re.DOTALL)
            c_text = regCleaning2.sub ("", c_text)
            c_text = c_text.replace (' & ', '_&_')
            c_text = c_text.replace ('\xa0', ' ')
            c_text = c_text.replace ('\r\n\t', '')
            c_text = c_text.replace ('.', ' ')
            c_text = c_text.replace ('—', '')
            c_text = c_text.replace ('"', '')
            c_text = c_text.replace (' - ', ' ')
            c_text = c_text.replace ('   ', ' ')
            c_text = c_text.replace ('  ', ' ')
            c_text = c_text.lower ()
            c_text = c_text.split (' ')
            mnText = []
            for word in c_text:
                clean_text = word.strip (',.-?!:()«»"')
                if clean_text != '':
                    mnText.append (clean_text)
            mnText = set (mnText)
            if i == 1:
                commonWords = mnText
                uniqueWords = mnText
            else:
#                commonWords = commonWords.intersection (mnText)
                 commonWords = commonWords & mnText
#                uniqueWords = uniqueWords.symmetric_difference (mnText)
                 uniqueWords = uniqueWords ^ mnText
            i += 1
            
    f = open ('CommonWords.txt', 'w', encoding = 'utf-8')
    for element in commonWords:
        f.write (element + '\n')
    f.close ()

    f2 = open ('UniqueWords.txt', 'w', encoding = 'utf-8')
    for element in uniqueWords:
        f2.write (element + '\n')
    f2.close ()
    
    return


def w_files ():
    f = open ('CommonWords.txt', 'r', encoding = 'utf-8')
    strings1 = f.readlines ()
    strings1.sort()
    f.close ()
    f = open ('CommonWords.txt', 'w', encoding = 'utf-8')
    for element in strings1:
        f.write (element)
    f.close ()
    
    f2 = open ('UniqueWords.txt', 'r', encoding = 'utf-8')
    strings2 = f2.readlines ()
    strings2.sort()
    f2.close ()
    f2 = open ('UniqueWords.txt', 'w', encoding = 'utf-8')
    for element in strings2:
        f2.write (element)
    f2.close ()

    
def main():
    val1 = download_search_set_write (URL)
    val2 = w_files()

if __name__ == '__main__' :
    main()
