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
            c_text = c_text.replace (' & ', '_&_') #Чтобы название альбома не разбивалось.
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
            d = {}
            freq = []
            for element in mnText:
                if element in d:
                    d [element] += 1
                else:
                    d [element] = 1
            for element in d:
                if d[element] > 1:
                    freq.append (element)
            freq = set (freq)
            
            mnText = set (mnText)
            if i == 1:
                commonWords = mnText
                uniqueWords = mnText
                freqWords = freq
            else:
#                commonWords = commonWords.intersection (mnText)
                commonWords = commonWords & mnText
#                uniqueWords = uniqueWords.symmetric_difference (mnText)
                uniqueWords = uniqueWords ^ mnText
                freqWords = freqWords ^ freq
            i += 1

    freqWords = freqWords & uniqueWords
    commonWords = list (commonWords)
    commonWords.sort()
    uniqueWords = list (uniqueWords)
    uniqueWords.sort()
    freqWords = list (freqWords)
    freqWords.sort()
    
    f = open ('CommonWords.txt', 'w', encoding = 'utf-8')
    for element in commonWords:
        f.write (element + '\n')
    f.close ()

    f2 = open ('UniqueWords.txt', 'w', encoding = 'utf-8')
    for element in uniqueWords:
        f2.write (element + '\n')
    f2.close ()
    
    f3 = open ('FrequentWords.txt', 'w', encoding = 'utf-8')
    for element in freqWords:
        f3.write (element + '\n')
    f3.close ()
    
    return

    
def main():
    val1 = download_search_set_write (URL)

if __name__ == '__main__' :
    main()
