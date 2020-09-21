from flask import Flask

app = Flask(__name__)  # takes current module name as argument

# variable rule
@app.route('/hello/<name>')
def hello_world(name):
    return 'hello {0}'.format(name)

# accepts only int type variable rule
@app.route('/blog/<int:post_id>')
def show_blog(post_id):
    return 'post id:{0}'.format(post_id)

# accepts only float type variable rule
@app.route('/rev/<float:revision_number>')
def show_revno(revision_number):
    return 'revision number:{0}'.format(revision_number)

# canonical URL
# here /python and /python/ both will work
@app.route('/python/')
def hello_python():
    return 'hello python'


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='127.0.0.1', port=5000, debug=True)
