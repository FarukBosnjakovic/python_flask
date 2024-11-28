from flask import Flask
from flask import render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user 


app = Flask(__name__)
app.secret_key = 'faruk123'

'''CONNECT TO DB'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy()
db.init_app(app)


'''CONFIGURE Flask-Login's Login Manager'''
login_manager = LoginManager()
login_manager.init_app(app) 


'''Create a user loader callback'''
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


'''Create table in DB with the UserMixin'''
class User(UserMixin, db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    
with app.app_context():
    db.create_all()
    


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        email = request.form.get('email') 
        result = db.session.execute(db.Select(User).where(User.email == email)) 
        
        # Note, email in db is unique so will only have one result 
        user = result.scalar() 
        if user:
            # Korisnik vec postoji 
            flash('Email postoji! Prijavite se...') 
            return redirect(url_for('login')) 

        # Hashing and Salting the password entered by the user 
        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method = 'pbkdf2:sha256',
            salt_length=8
        )
        
        # Storing the password in our database 
        new_user = User(
            email = request.form.get('email'),
            name = request.form.get('name'),
            password = hash_and_salted_password,
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Log in and authenticate user adding details to database 
        login_user(new_user) 
        
        return render_template('secrets.html') 
    
    # Passing True or False if the user is authenticated
    return render_template('register.html', logged_in = current_user.is_authenticated)


@app.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password') 
        
        # Find user by email entered 
        result = db.session.execute(db.select(User).where(User.email == email)) 
        user = result.scalar() 
        
        # Email doesn't exist or password incorrect 
        if not user:
            flash('Email ne postoji, pokusajte ponovo') 
            return redirect(url_for('login')) 
        elif not check_password_hash(user.password, password):
            flash('Lozinka netacna, pokusajte ponovo') 
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('secrets'))
        
        # check stored password has against entered password hashed
        
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('secrets')) 
    
    # Passing True or False if the user is authenticated
    return render_template('login.html', logged_in = current_user.is_authenticated)


@app.route('/secrets')
@login_required
def secrets():
    print(current_user.name)
    
    # Passing the name from the current_user 
    return render_template('secrets.html', name=current_user.name, logged_in=True)


@app.route('/logout') 
def logout():
    logout_user()
    return redirect(url_for('home')) 


# Only logged-in users can download the pdf 
@app.route('/download')
@login_required 
def download():
    return send_from_directory(directory='static', path='files/cheat_sheet.pdf')
            

if __name__ == "__main__":
    app.run(debug=True)