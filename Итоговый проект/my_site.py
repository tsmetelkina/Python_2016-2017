import json
from flask import Flask
from flask import url_for, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

#if __name__ == '__main__':
#    app.run(debug=True)

if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
