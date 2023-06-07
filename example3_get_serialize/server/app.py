from flask import Flask, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db
from models import Pet

# debug configuration instructions https://code.visualstudio.com/docs/python/tutorial-flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False  # print on separate lines with indentation

migrate = Migrate(app, db)

db.init_app(app)

if __name__ == '__main__':
    app.run(port=5555, debug=True)


@app.route('/')
def index():
    return '<h1>Welcome to the Pet App</h1>'

# jsonify called automatically on any dictionary passed to view


@app.route('/pets')
def pets():
    """
    pets = []  # create empty dictionary
    for pet in Pet.query.all():
        pets.append(pet.to_dict())
    """

    pets = [pet.to_dict() for pet in Pet.query.all()]
    return make_response(pets, 200)


@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()
    if pet is None:
        response_body = {'message': f'Pet {id} does not exist in database.'}
        return make_response(response_body, 404)  # 404 not found
    else:
        response_body = pet.to_dict()
        return make_response(response_body, 200)


@app.route('/species/<string:species>')
def pet_by_species(species):
    """
    pets = []  # create empty dictionary
    for pet in Pet.query.filter(Pet.species == species).all():
        pets.append(pet.to_dict(rules=('-species',)))
    """

    pets = [pet.to_dict(rules=('-species',))
            for pet in Pet.query.filter(Pet.species == species).all()]
    response_body = {'count': len(pets), 'pets': pets}
    return make_response(response_body, 200)
