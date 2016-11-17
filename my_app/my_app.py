import json
from flask import Flask
from flask import url_for, render_template, request, redirect

app = Flask(__name__)

filename = 'data2.txt'
file_json_name = 'data_json.txt'
@app.route('/')
def index():
    urls = {'Поиск по сайту': url_for('search'),
            'Статистика': url_for('stats'),}
   
    return render_template('index.html', urls=urls)



@app.route('/thanks')
def thanks():
    string = request.args.get ('email') + ';' + request.args.get ('lang') + ';' + request.args.get ('a_lang') + ';' + request.args.get ('color1') + ';' + request.args.get ('color2') + ';' + request.args.get ('color3') + ';' + request.args.get ('color4') + ';' + request.args.get ('color5') + ';' + request.args.get ('color6') + ';' + request.args.get ('color7') + ';' + request.args.get ('color8') + ';' + request.args.get ('color9') + ';' + request.args.get ('color10') + ';' + request.args.get ('color11') + ';' + request.args.get ('color12') + ';' + request.args.get('color13')
    out = open (filename, 'a', encoding = 'utf-8')
    out.write (string + '\n')
    out.close()
#    a = [request.args.get ('email'), request.args.get ('lang'), request.args.get ('a_lang'), request.args.get ('color1'), request.args.get ('color2'), request.args.get ('color3'), request.args.get ('color4'), request.args.get ('color5'), request.args.get ('color6'), request.args.get ('color7'), request.args.get ('color8'), request.args.get ('color9'), + request.args.get ('color10'), request.args.get ('color11'), request.args.get ('color12'), request.args.get('color13')]
#    f = open(file_json_name, 'w', encoding = 'utf-8')
#    json.dump(a, f) на этом моменте программа зависает, страница грузится, но не загружается
#    f.close()
    if request.args:
        email = request.args['email']
        lang = request.args['lang']
        a_lang = request.args['a_lang']
        color1 = request.args['color1']
        color2 = request.args['color2']
        color3 = request.args['color3']
        color4 = request.args['color4']
        color5 = request.args['color5']
        color6 = request.args['color6']
        color7 = request.args['color7']
        color8 = request.args['color8']
        color9 = request.args['color9']
        color10 = request.args['color10']
        color11 = request.args['color11']
        color12 = request.args['color12']
        color13 = request.args['color13']
        
        return render_template('thanks.html', email = email, lang = lang, a_lang = a_lang, color1 = color1, color2 = color2, color3 = color3, color4 = color4, color5 = color5, color6 = color6, color7 = color7, color8 = color8, color9 = color9, color10 = color10, color11 = color11, color12 = color12, color13 = color13)
 
#@app.route ('/json')
#def j_son():
#    out = open (file_json_name, r, encoding = 'utf-8')
#    j = readlines (out)
#    return j

@app.route('/stats')
def stats():
    i = 0
    out = open (filename, 'r', encoding = 'utf-8')
    for line in out:
        i += 1
    out.close()
    numbers = i
    a = []
    lang = ''
    out2 = open (filename, 'r', encoding = 'utf-8')
    for line in out2:
        if line != '\n':
            line.strip ('\n')
            answers = line.split (';')
            a.append (answers[1])    
    lan = set (a)
    for element in lan:
        lang = element + ', ' + lang
    lang = lang.strip (', ')
    out2.close()

    return render_template('stats.html', numbers = numbers, lang = lang) 

@app.route('/search')
def search():
    
    return render_template ('search.html')


@app.route ('/results')
def results ():
    i = 1
    a = []
    col = []
    result = ''
    for i in range (1, 14):
        if request.args.get ('color%s' %(str(i))) == 'on':

            out2 = open (filename, 'r', encoding = 'utf-8')
            for line in out2:
                if line != '\n':
                    line = line.strip ('\n')
                    answers = line.split (';')
                    col.append (answers[2 + i] + ' (' + answers[1] + ')')
        i += 1   
    for element in col:
        if element not in a:
            a.append (element)
    for element in a:
        result = element + ', ' + result
    result = result.strip (', ')
    
    return render_template ('search_result.html', result = result)


if __name__ == '__main__':
    app.run(debug=True)
