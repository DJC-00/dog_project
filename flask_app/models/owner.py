from pickle import FALSE
from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASS_REGEX = re.compile(r'^(?=.*[0-9]+.*)(?=.*[a-zA-Z]+.*)[0-9a-zA-Z]{6,}$')

from flask_app.models import dog

class Owner:
    db = "dogs_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]

        self.id = data["id"]
        self.id = data["id"]

        self.dogs = []

#--------------------( Static Methods )--------------------#

#######################( Validation )#######################

    @staticmethod
    def validate_registration(raw_form_data):
        is_valid = True

        # Check first_name
        if len(raw_form_data["first_name"]) < 2:
            flash("Invalid First Name: Must be at least 2 characters long")
            is_valid = False

        # Check last_name
        if len(raw_form_data["last_name"]) < 2:
            flash("Invalid Last Name: Must be at least 2 characters long")
            is_valid = False

        if not Owner.email_validation(raw_form_data["email"]):
            is_valid = False

        if not Owner.password_validation(raw_form_data["password"], raw_form_data["pass_confirm"], True):
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(raw_form_data):
        isValid = True
        owner_from_db = Owner.get_owner_by_email(raw_form_data)
        print(owner_from_db)
        if not owner_from_db:
            flash("Invalid Email or Password")
            isValid = False
        elif not Bcrypt.check_password_hash(Owner, owner_from_db.password , raw_form_data['password']):
            flash("Invalid Email or Password")
            isValid = False

        
        return isValid


    @staticmethod
    def email_validation(form_email):
        email_valid = True

        email_list = Owner.get_all_emails(form_email)

        if not EMAIL_REGEX.match(form_email):
            flash("Invalid Email: Please enter a valid Email Address")
            email_valid = False
            return email_valid

        for email in email_list:
            db_email = email['email']
            if db_email == form_email:
                print(db_email == form_email)
                flash(f"Error: Account with {form_email} already exists.")
                email_valid = False
                return email_valid
            else:
                print("db_email == form_email")
                continue

        return email_valid

    @staticmethod
    def password_validation(password, pass_confirm, reg = False):
        pass_valid = True
        if reg == True:
            if not PASS_REGEX.match(password):
                flash("Invalid Password: Password must contain at least one letter, at least one number, and be longer than six charaters.")
                pass_valid = False
                return pass_valid

        # Check password against pass_confirm
        if(password != pass_confirm):
            flash("Invalid Password: Passwords do not match")
            pass_valid = False
            return pass_valid
        return pass_valid

#--------------------( Class Methods )--------------------#
    @classmethod
    def create_owner(cls, data):
        query = """INSERT INTO owners (first_name, last_name, email, password, created_at, updated_at) 
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW() );"""

        queryResult = connectToMySQL(cls.db).query_db(query,data)
        return queryResult

    @classmethod
    def get_all_emails(cls, form_email):

        query = ("SELECT owners.email FROM owners;")

        email_list = connectToMySQL(cls.db).query_db(query)

        return email_list

    @classmethod
    def get_owner_by_ID(cls,data):
        query = """SELECT * FROM owners WHERE id = %(id)s"""
        query_result = connectToMySQL(cls.db).query_db(query,data)
        if len(query_result) < 1:
            return False

        return (cls(query_result[0]))
    
    @classmethod
    def get_owner_by_email(cls,data):
        query = """SELECT * FROM owners WHERE email = %(email)s"""
        query_result = connectToMySQL(cls.db).query_db(query,data)
        if len(query_result) < 1:
            return False

        return (cls(query_result[0]))