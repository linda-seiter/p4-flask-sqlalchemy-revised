from flask import Flask, make_response, jsonify, request
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


@app.route('/pets', methods=['GET', 'POST'])
def pets():
    if request.method == 'GET':
        pets = [pet.to_dict() for pet in Pet.query.all()]
        return make_response(pets, 200)

    elif request.method == 'POST':
        new_pet = Pet(name=request.form.get('name'),
                      species=request.form.get('species'))
        db.session.add(new_pet)
        db.session.commit()
        pet_dict = new_pet.to_dict()
        # new_pet.to_dict() should be called after commit so id value is available
        return make_response(pet_dict, 201)


@app.route('/pets/<int:id>', methods=['GET', 'DELETE', 'PATCH'])
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()

    if pet is None:
        not_found = {'message': f'Pet {id} does not exist in database.'}
        return make_response(not_found, 404)  # 404 not found

    elif request.method == 'GET':
        pet_dict = pet.to_dict()
        return make_response(pet_dict, 200)

    elif request.method == 'DELETE':
        db.session.delete(pet)
        db.session.commit()
        success = {
            "delete_successful": True,
            "message": f'Pet {id} deleted'
        }
        return make_response(success, 200)


@app.route('/species/<string:species>')
def pet_by_species(species):
    """
    pets = []  # create empty dictionary
    for pet in Pet.query.filter(Pet.species == species).all():
        pets.append(pet.to_dict(rules=('-species',)))
    """

    pets = [pet.to_dict(rules=('-species',))
            for pet in Pet.query.filter(Pet.species == species).all()]
    response = {'count': len(pets), 'pets': pets}
    return make_response(response, 200)
