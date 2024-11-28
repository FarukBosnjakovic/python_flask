from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5 
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, SelectField
from wtforms import Form 
from wtforms.validators import DataRequired, URL 
import csv 
from coffee_form import CafeForm


app = Flask(__name__)
app.secret_key = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)


@app.route('/')
def home():
    return render_template('index.html') 


@app.route('/add', methods=['GET', 'POST']) 
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', mode='a', encoding='utf-8') as csv_file:
            csv_file.write(f"\n{form.cafe.data})," # "cafe" je varijabla iz klase "CafeForm"
                           f"{form.location.data},"
                           f"{form.open.data},"
                           f"{form.close.data},"
                           f"{form.coffee_rating.data},"
                           f"{form.wifi_rating.data},"
                           f"{form.power_rating.data}") 
        return redirect(url_for('cafes')) 
    return render_template('add.html', form=form)
            

@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',') 
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == "__main__":
    app.run(debug=True)           