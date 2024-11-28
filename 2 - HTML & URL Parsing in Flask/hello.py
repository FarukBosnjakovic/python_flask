from flask import Flask 

app = Flask(__name__)

@app.route('/')
def hello_world(): 
    return "Hello, World!" 


@app.route('/bye') 
def bye(): 
    return "Bye!"


@app.route('/username/<name>')
def greet(name): 
    return f'Hello {name}!'


@app.route('/username1/<path:name>') 
def greet1(name):
    return f'Hello there {name}!'


# Creating variable paths and converting the path to a specified data type 
@app.route('/username2/<name>/<int:number>') 
def greet2(name, number):
    return f'Hello there {name}, you are {number} years old!'


if __name__ == "__main__":
    app.run(debug=True)