from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def search():
    movie = request.form['movie']
    return movie


if __name__ == "__main__":
    app.run()
