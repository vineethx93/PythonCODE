from flask import Flask

app = Flask(__name__)  # takes current module name as argument


@app.route('/')
def hello_world():
    return 'hello world'


if __name__ == '__main__':
    app.run()
    # app.run(host='127.0.0.1', port=5000, debug=True)
