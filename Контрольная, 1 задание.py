import urllib.request
import re
import os
from os import listdir

def searching ():
    Thai = []
    Eng = []

    for file in os.listdir("."): #Файл с кодом (.py) должен лежать в папке с нужными файлами .html
        f = open (file, 'r', encoding = 'utf-8')
        _f_ = f.read ()
        if _f_ != "":
            regThai = re.compile ("<a href='/id/[0-9]*[^>]*?'>([^< ]*?)</a>", flags=re.U | re.DOTALL)
            thaiWord = regThai.findall (_f_)
            del thaiWord[0]
            del thaiWord[0]
#            for element in thaiWord:
#                print (element)
            regEng = regThai = re.compile ("<td>([][ )(;0-9a-zA-Z\,]*)</td>", flags=re.U | re.DOTALL) #Не ищет определения, содержащие тайские символы, и из-за этого словарь "съезжает"
            engWord = regEng.findall (_f_)
            del engWord[0]
            del engWord[0]
#            for element in engWord:
#                print (element)
            d = dict(zip(thaiWord, engWord))
            #print (d)
            return d

searching ()
