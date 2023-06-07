from flask import Flask, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db
from models import Pet

# debug configuration instructions https://code.visualstudio.com/docs/python/tutorial-flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

if __name__ == '__main__':
    app.run(port=5555, debug=True)


@app.route('/')
def index():
    return '<h1>Welcome to the Pet App</h1>'


@app.route('/pets')
def pets():
    pets = Pet.query.all()
    response_body = '<h2>Pets</h2>'
    for pet in pets:
        response_body += f'<p>{pet.id}  {pet.name}   {pet.species}  </p>'
    response = make_response(response_body, 200)
    return response


@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()
    response_body = '<h2>Pet</h2>'
    if pet:
        response_body += f'<p>{pet.name}   {pet.species}  </p>'
    else:
        response_body += f'No pet with id {id}'
    response = make_response(response_body, 200)
    return response


@app.route('/species/<string:species>')
def pet_by_species(species):
    # all() returns query result as a list so we can get len
    pets = Pet.query.filter(Pet.species == species).all()
    size = len(pets)
    response_body = f'<h2>There are {size} {species}s</h2>'
    for pet in pets:
        response_body += f'<p>{pet.id}  {pet.name} </p>'
    response = make_response(response_body, 200)
    return response
