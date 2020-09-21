from flask import Flask, redirect, url_for, request

app = Flask(__name__)


@app.route('/login/<name>/')
def success(name):
    return 'welcome {0}'.format(name)


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success', name=user))
    elif request.method == 'GET':
        user = request.args.get('nm')
        return redirect(url_for('success', name=user))


if __name__ == '__main__':
    app.run(debug=True)