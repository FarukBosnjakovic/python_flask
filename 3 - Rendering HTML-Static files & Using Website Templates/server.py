from flask import Flask 
from flask import render_template

app = Flask(__name__)

# How to render a web page which is rendered inside of a HTML file 
@app.route('/')
def hello():
    return render_template("index.html") 

@app.route('/bye')
def name():
    return render_template("index2.html")


if __name__ == "__main__":
    app.run(debug=True)