from flask import Flask, render_template, redirect, url_for
from phoneme_example_dict import phoneme_words

app = Flask(__name__)

app.add_url_rule("/favicon", "favicon", lambda: redirect(url_for("static", filename="favicon/favicon.ico")))
app.add_url_rule("/favicon-16x16", "favicon-16x16",
                 lambda: redirect(url_for("static", filename="favicon/favicon-16x16.png")))
app.add_url_rule("/favicon-32x32", "favicon-32x32",
                 lambda: redirect(url_for("static", filename="favicon/favicon-32x32.png")))
app.add_url_rule("/apple-touch-icon", "apple-touch-icon",
                 lambda: redirect(url_for("static", filename="favicon/apple-touch-icon.png")))
app.add_url_rule("/site_webmanifest", "site_webmanifest",
                 lambda: redirect(url_for("static", filename="favicon/site.webmanifest")))


@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for("synthesiser"))


@app.route('/synthesiser')
def synthesiser():
    return render_template("synthesiser.html")


@app.route('/concatenation_setup')
def concatenation_setup():
    return render_template("concatenation_setup.html", phoneme_words=phoneme_words)


@app.route('/ml_setup')
def ml_setup():
    return render_template("ml_setup.html")


if __name__ == '__main__':
    app.run()
