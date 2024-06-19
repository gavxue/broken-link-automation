from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/check', methods=['POST'])
def check():
    if request.method == 'POST':
        url = request.values.get('url')
        return render_template('check.html', url=url)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug = True)