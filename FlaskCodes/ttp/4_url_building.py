from flask import Flask, redirect, url_for

app = Flask(__name__)


@app.route('/admin/')
def hello_admin():
    return 'hello admin'


@app.route('/guest/<guest_name>/')
def hello_guest(guest_name):
    return 'hello {0} as guest'.format(guest_name)


@app.route('/user/<name>')
def hello_user(name):
    if name == 'admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_guest', guest_name=name))


if __name__ == '__main__':
    app.run(debug=True)

