from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for("synthesiser"))


@app.route('/synthesiser')
def synthesiser():
    return render_template("synthesiser.html")


@app.route('/concatenation_setup')
def concatenation_setup():
    return render_template("concatenation_setup.html")


@app.route('/ml_setup')
def ml_setup():
    return render_template("ml_setup.html")


if __name__ == '__main__':
    app.run()
