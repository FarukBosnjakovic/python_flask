from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap5
from datetime import date
from forms import CreatePostForm


app = Flask(__name__)
app.secret_key = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
bootstrap = Bootstrap5(app)


'''CONNECT TO DB'''

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy()
db.init_app(app)


'''CONFIGURE TABLE'''

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)

# with app.app_context():
#     db.create_all()



'''ROUTES'''

@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost)) 
    posts = result.scalars().all()
    return render_template('index.html', all_posts=posts)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')



@app.route('/post/<int:post_id>') 
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    return render_template('post.html', post=requested_post)


@app.route('/new-post', methods=['GET', 'POST']) 
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit(): 
        new_post = BlogPost(
            title = form.title.data,
            subtitle = form.subtitle.data,
            body = form.body.data,
            author = form.author.data,
            date = date.today().strftime("%B %d, %Y")
        )
        
        db.session.add(new_post)
        db.session.commit() 
        
        return redirect(url_for('get_all_posts')) 
    return render_template('make-post.html', form=form)


@app.route('/edit-post/<int:post_id>', methods=['GET', 'POST']) 
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title = post.title,
        subtitle = post.subtitle,
        author = post.author,
        body = post.body
    )
    
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data



if __name__ == "__main__":
    app.run(debug=True)