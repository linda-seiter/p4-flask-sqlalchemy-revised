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


@app.route('/pets')
def pets():
    pets = []  # create empty dictionary
    for pet in Pet.query.all():
        pet_dict = {'id': pet.id,
                    'name': pet.name,
                    'species': pet.species,
                    }
        pets.append(pet_dict)

    response = make_response(jsonify(pets), 200)
    return response


@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()
    if pet is None:
        response = {'message': f'Pet {id} does not exist in database.'}
        response = make_response(jsonify(response), 404)
    else:
        response_body = {'id': pet.id,
                         'name': pet.name, 'species': pet.species}
        response = make_response(jsonify(response_body), 200)
    return response


@app.route('/species/<string:species>')
def pet_by_species(species):
    pets = []  # create empty dictionary
    for pet in Pet.query.filter(Pet.species == species).all():
        pet_dict = {'id': pet.id,
                    'name': pet.name,
                    }
        pets.append(pet_dict)
    response_body = {'count': len(pets), 'pets': pets}
    response = make_response(jsonify(response_body), 200)
    return response
