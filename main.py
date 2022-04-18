from flask import Flask, redirect, url_for

app = Flask(__name__)


@app.route("/")
def home():
    return "This is Avraham page <h1>Title<h1>"


@app.route("/<name>")
def user(name):
    return f"Hello {name}!"

@app.route("/admin")
def admin():
    return redirect(url_for("homdfsdf"))


if __name__ == "__main__":
    app.run()
