from flask import Flask, render_template
import random 
import datetime 
import requests

app = Flask(__name__) 

@app.route('/') 
def hello():
    random_number = random.randint(1, 10) 
    current_year = datetime.datetime.now().year
    return render_template("index.html", num=random_number, year=current_year) 


@app.route('/guess/<name>') 
def guess(name): 
    '''get an API to return names'''
    name_url = requests.get(f'https://api.agify.io?name={name}')
    name_url.raise_for_status() 
    names_data = name_url.json() 
    names = names_data["name"] 
    
    '''get an API to return genders'''
    gender_url = requests.get(f'https://api.genderize.io?name={name}')
    gender_url.raise_for_status() 
    gender_data = gender_url.json() 
    genders = gender_data["gender"]
    
    '''get an API for age of a person'''
    age_url = requests.get(f'https://api.agify.io?name={name}')
    age_url.raise_for_status()
    age_data = age_url.json()
    age = age_data["gender"] 
    
    return render_template("names.html", name=names, gender=genders, age=age) 


@app.route('/blog/<num>') 
def get_blog(num): 
    blog_url = 'https://api.npoint.io/c790b4d5cab58020d391'
    blog_data = requests.get(blog_url) 
    all_posts = blog_data.json()
    return render_template("blog.html", posts=all_posts) 


if __name__ == "__main__":
    app.run(debug=True)