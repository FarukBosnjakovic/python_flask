from flask import Flask, render_template
from flask import request
import requests 
import smtplib 

app = Flask(__name__)

posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()
OWN_EMAIL = "YOUR OWN EMAIL ADDRESS"
OWN_PASSWORD = "YOUR EMAIL ADDRESS PASSWORD"


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route('/about') 
def about():
    return render_template("about.html") 


@app.route('/login', methods=['POST']) 
def receive_data(): 
    '''return "Successful form submitted'''
    name = request.form['username'] 
    password = request.form['password'] 
    return f"<h1>Name: {name}, Password: {password}</h1>"


@app.route('/contact', methods=['GET', 'POST']) 
def contact():
    if request.method == 'POST':
        data = request.form 
        send_email(data['name'], data['email'], data['phone'], data['message']) 
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


def send_email(name, email, phone, message): 
    email_message = f'Subject:New message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}' 
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_PASSWORD, email_message)


@app.route('/post/<int:index>') 
def show_post(index):
    requested_post = None 
    for blog_post in posts:
        if blog_post['id'] == index:
            requested_post = blog_post
    return render_template('post.html', post=requested_post)


if __name__ == "__main__":
    app.run(debug=True)