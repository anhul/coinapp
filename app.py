from flask import Flask

app = Flask(__name__)


@app.route('/tasks')
def get_tasks():
    return 'list of tasks'
