import os
name = 'new 1.txt'

def file_for_insert (name):
    
    f = open (name, 'r', encoding = 'utf-8')
    lines = f.readlines()
    f.close ()
    for line in lines:
        line = line.replace (' - ', '- ')
        words = line.split()
        
        for word in words:
            if word != "":
                string = word + '\n'
                ff = open ('input2.txt', 'a', encoding = 'utf-8')
                ff.write (string)
                ff.close()
    os.system(r"C:\Users\Tais\Desktop\mystem.exe input2.txt output2.txt -nld --format text")
    return


def _insert_ ():
    d = {}
    f = open ('input2.txt', 'r', encoding = 'utf-8')
    lines_token = f.read()
    f.close ()
    lines_token = lines_token.split ('\n')
    del lines_token[-1]

    ff = open ('output2.txt', 'r', encoding = 'utf-8')
    lines_lemma = ff.read()
    ff.close ()
    lines_lemma = lines_lemma.split ('\n')
    del lines_lemma[-1]

    
    j = 0
    for token, lemma in zip(lines_token, lines_lemma):

        token_l = token.lower()
        token_cl = token_l.strip (',.-?!;:()«»"')
        d[token_cl] = lemma

    for token in d:
        j += 1
        string2 = 'INSERT INTO The_Second_Table (ID, Token, Lemma) VALUES ("%d", "%s", "%s");\n' %(j, token, d[token])
        d[token] = j
        f3 = open ('insert2.txt', 'a', encoding = 'utf-8')
        f3.write (string2)
        f3.close()
 
    i = 1
    for token in lines_token:
        if token[0] == '"' and token[0] == '«' and token[0] == '(': #Возможно, я не совсем правильно поняла, что такое "знак слева".
            punkt_left = token[0]
        else:
            punkt_left = 0
            
        if token[-1] == '"' or token[-1] == '»' or token[-1] == ',' or token[-1] == '.' or token[-1] == ';' or token[-1] == ':' or token[-1] == '-' or token[-1] == '?' or token[-1] == '!':  
            punkt_right = token[-1]
        else:
            punkt_right = 0
            
        t = token.lower()
        t = t.strip (',.-?!;:()«»"')
        for token_cl in d:
            if t == token_cl:
                string = 'INSERT INTO The_First_Table (Token, Punkt_mark_left, Punkt_mark_right, Token_num, Token_ID) VALUES ("%s", "%s", "%s", "%d", "%d");\n' %(token.strip (',.-?!;:()«»"'), punkt_left, punkt_right, i, d[token_cl])
            else:
                continue
        f3 = open ('insert2.txt', 'a', encoding = 'utf-8')
        f3.write (string)
        f3.close()
        i += 1
    return

def main():
    val1 = file_for_insert (name)
    val2 = _insert_ ()

    
if __name__ == '__main__' :
    main()
