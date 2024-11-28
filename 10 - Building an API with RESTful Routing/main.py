from flask import Flask 
from flask import jsonify, render_template, request 
from flask_sqlalchemy import SQLAlchemy
import random 


app = Flask(__name__) 


# Connect to DB 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)


# Cafe TABLE Configuration

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=True)
    img_url = db.Column(db.String(500), nullable=True)
    location = db.Column(db.String(500), nullable=True)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)
    
    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

with app.app_context():
    db.create_all()
    

'''ROUTES'''

@app.route('/') 
def home():
    return render_template('index.html')


@app.route('/random') 
def get_radnom_cafe():
    result = db.session.execute(db.select(Cafe)) 
    all_cafes = result.scalars().all() 
    random_cafe = random.choice(all_cafes)
    return jsonify(Cafe={
        "id": random_cafe.id,
        "name": random_cafe.name,
        "map_url": random_cafe.map_url,
        "img_url": random_cafe.img_url,
        "location": random_cafe.location,
        "seats": random_cafe.seats,
        "has_toilet": random_cafe.has_toilet,
        "has_wifi": random_cafe.has_wifi,
        "has_sockets": random_cafe.has_sockets,
        "can_take_calls": random_cafe.can_take_calls,
        "coffee_price": random_cafe.coffee_price,
    })


'''GET ALL CAFES'''

@app.route('/all')
def get_all_cafes():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name)) 
    all_cafes = result.scalars().all()
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes]) 


'''FIND A CAFE'''

@app.route('/search')
def get_cafe_at_location():
    query_location = request.args.get('loc')
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    all_cafes = result.scalars().all() 
    if all_cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at your location."}), 404
    
    

'''POST - Add New Coffee'''

@app.route('/add', methods=['POST']) 
def post_new_cafe():
    new_cafe = Cafe(
        name = request.form.get("name"),
        map_url = request.form.get('map_url'),
        img_url = request.form.get('img_url'),
        location = request.form.get('location'),
        has_sockets = bool(request.form.get('has_sockets')),
        has_toilet = bool(request.form.get('has_toilet')),
        has_wifi = bool(request.form.get('has_wifi')),
        can_take_calls = request.form.get('can_take_calls'),
        seats = bool(request.form.get('seats')),
        coffee_price = request.form.get('coffee_price')
    )
    
    db.session.add(new_cafe)
    db.session.commit()
    
    return jsonify(response={"Success": "Successfully added new cafe."}) 


'''PATCH - Update Coffee Price'''
# Updating the price of a cafe based on a particular 'id':

@app.route('/update-price/<int:cafe_id>', methods=['PATCH']) 
def patch_new_price(cafe_id): 
    new_price = request.args.get('new_price')
    cafe = db.get_or_404(Cafe, cafe_id) 
    if cafe:
        cafe.coffee_price = new_price 
        
        db.session.commit() 
        
        return jsonify(response={"Success": "Successfully updated the price."}), 200
    else:
        return jsonify(error={"Not found": "Sorry, a cafe with that id was not found in the database."}), 404 
    
    
'''DELETE - Delete a Cafe'''
app.route('/report-closes/<int:cafe_id>', methods=['DELETE']) 
def delete_cafe(cafe_id):
    api_key = request.args.get('api_key') 
    if api_key == 'API_KEY':
        cafe = db.get_or_404(Cafe, cafe_id)
        if cafe:
            
            db.session.delete(cafe)
            db.session.commit()
            
            return jsonify(response = {"Success": "Successfully deleted the cafe from the database."}), 200
        else:
            return jsonify(error = {"Not found": "Sorry, a cafe with that ud was not found in the database."}), 404 
    else:
        return jsonify(error={"Forbidden": "Sorry, that's now allowed. Make sure you have correct API KEY"}), 403



if __name__ == "__main__":
    app.run(debug=True)