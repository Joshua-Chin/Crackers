from flask import Flask, request, session

from database import db_session

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return 'Hello World'

@app.route('/api', methods=['POST'])
def api():
    pass

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run()
