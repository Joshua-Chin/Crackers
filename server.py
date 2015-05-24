from flask import Flask, request, session

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return 'Hello World'

@app.route('/api', methods=['POST'])
def api():
    pass

if __name__ == '__main__':
    app.run()
