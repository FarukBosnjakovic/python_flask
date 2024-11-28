# Rendering HTML Elements

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/') 
def index():
    return render_template("index.html") 

@app.route('/hello') 
@app.route('/hello/<name>') 
def hello(faruk):
    return render_template("index.html", name=faruk)


if __name__ == "__main__":
    app.run(debug=True)