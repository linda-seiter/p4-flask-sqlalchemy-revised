from random import choice as rc

from faker import Faker

from app import app
from models import db, Pet

fake = Faker()

with app.app_context():

    Pet.query.delete()

    pets = []
    species = ['Dog', 'Cat', 'Chicken', 'Hamster', 'Turtle']
    for n in range(100):
        pet = Pet(name=fake.first_name(), species=rc(species))
        pets.append(pet)

    db.session.add_all(pets)
    db.session.commit()
