from flask import Flask, render_template

application = Flask(__name__)

@application.route('/')
@application.route('/<username>/')
def index(username=None):
    if username:
        return render_template("aboutme.html", page_title=username)
    return render_template("index.html", page_title='About me')

if __name__ == '__main__':
    application.run(debug=True, host="0.0.0.0", port=8888)