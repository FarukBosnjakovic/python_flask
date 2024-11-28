from flask import Flask 

app = Flask(__name__) 

@app.route('/')
def hello_world():
    return '<h1>Hello, World</h1>'\
        '<p>This is a paragraph</p><br>'\
            '<img src="https://media.giphy.com/media/yFQ0ywscgobJK/giphy.gif" width=200>'
            

# Make different decorator functions

def make_bold(function):
    def wrapper():
        return "<b>" + function() + "</b>"
    return wrapper
    
def make_emphasis(function):
    def wrapper():
        return "<em>" + function() + "</em>"
    return wrapper

def make_italic(function):
    def wrapper():
        return "<u>" + function() + "</u>"
    return wrapper 


@app.route('/bye') 
@make_bold
@make_emphasis
@make_italic
def bye():
    return "Bye!"


@app.route('/username/<name>')
def greet(name):
    return f'Hello {name}'


@app.route('/username1/<path:name>') 
def greet1(name):
    return f'Hello there {name}!'



if __name__ == "__main__":
    app.run(debug=True)