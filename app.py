from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/check')
def check():
    return render_template('check.html')


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug = True)