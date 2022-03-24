from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app import app
bcrypt = Bcrypt(app)
from flask_app.models import owner


class Dog:
    db = "dogs_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.breed = data["breed"]
        self.age = data["age"]

        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.owner = {}


    @classmethod
    def get_all_dogs(cls):
        query = "SELECT * FROM dogs"
        query_result = connectToMySQL(cls.db).query_db(query)
        return query_result

    @classmethod
    def get_dogs_and_owners(cls):
        query = """SELECT dogs.id, dogs.name, dogs.breed, dogs.age, dogs.owners_id, dogs.created_at, dogs.updated_at, owners.id AS "owner_id", owners.first_name AS owner_fname, owners.last_name AS owner_lname, owners.email FROM dogs
                JOIN owners ON dogs.owners_id = owners.id
                ORDER BY dogs.id"""
        query_result = connectToMySQL(cls.db).query_db(query)
        all_dogs_with_owners = []
        for dog in query_result:
            all_dogs_with_owners.append( cls(dog))

        # for owner in query_result['dog']:
        #     print("jhe")
            # factionData = {
            # "id" : owner['owner.id'],
            # "name" : query_result[dog]["first_name"], # Do not use factions.[var] for non coliding fields
            # "last_name" : query_result[dog]["level"],
            # "email" : query_result[dog]["email"],
            # "created_at" : query_result[dog]["owners.created_at"],
            # "updated_at" : query_result[dog]["owners.updated_at"]
            # }

        # for each in all_dogs_with_owners:
        #     # print(each)
        return query_result

    @classmethod
    def get_dog_by_ID(cls,data):
        # print(query_data["id"])
        # query = """SELECT dogs.id, dogs.name, dogs.breed, dogs.age, dogs.owners_id, dogs.created_at, dogs.updated_at, owners.id AS "owner_id", owners.first_name AS owner_fname, owners.last_name AS owner_lname, owners.email FROM dogs
        #         JOIN owners ON dogs.owners_id = owners.id
        #         WHERE (dogs.id = %(id)s)
        #         ORDER BY dogs.id"""

        query = """SELECT * FROM dogs
        LEFT JOIN owners ON dogs.owners_id = owners.id
        WHERE dogs.id = %(id)s;"""

        query_result = connectToMySQL(cls.db).query_db(query,data)
        # print(query_result)
        if len(query_result) < 1:
            return False

        newdog = ( cls(query_result[0]))
        ownerData = {
        "id" : query_result[0]["owners.id"],
        "first_name" : query_result[0]["first_name"], # Do not use factions.[var] for non coliding fields
        "last_name" : query_result[0]["last_name"],
        "email" : query_result[0]["email"],
        "password" : query_result[0]["password"],
        "created_at" : query_result[0]["owners.created_at"],
        "updated_at" : query_result[0]["owners.updated_at"],
        }

        ownerInstance = owner.Owner(ownerData)
        newdog.owner = ownerInstance

        return newdog

    @classmethod
    def create_dog(cls,data):
        query = """INSERT INTO dogs (name, breed, age, created_at, updated_at, owners_id) VALUES (%(name)s, %(breed)s, %(age)s, NOW(), NOW(), %(owner_id)s);"""
        query_result = connectToMySQL(cls.db).query_db(query,data)
        return query_result

    @classmethod
    def edit_dog(cls,data):
        query = """UPDATE dogs SET name = %(name)s,breed = %(breed)s,age = %(age)s WHERE id = %(id)s ; """
        query_result = connectToMySQL(cls.db).query_db(query,data)
        return query_result

    @classmethod
    def delete_dog(cls,id):
        query = "DELETE FROM dogs WHERE `id` = %(id)s"
        query_result = connectToMySQL(cls.db).query_db(query,id)
        return query_result