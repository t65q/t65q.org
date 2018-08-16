from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():

    return render_template('index.html')

@app.route('/news', methods=['GET'])
def news():

    return "foo"

@app.route('/events', methods=['GET'])
def events():

    return "foo"

@app.route('/about', methods=['GET'])
def about():

    return "foo"

@app.route('/contact', methods=['GET'])
def contact():

    return "foo"