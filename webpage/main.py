# coding: utf-8
# %load main.py
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/lady/<guest>")
def lady(guest):
    return("gaga %s" % guest)

@app.route("/david")
def david():
    return("hasselhoff")

@app.route("/")
def index():
    return(render_template("index.html"))

if __name__ == '__main__':
    app.run(debug=True)
