from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.dog import Dog
from flask_app.models.owner import Owner

@app.route('/')
def login_registration_page():
    return render_template('log_and_reg.html')

@app.route('/login', methods=['POST'])
def owner_login():
    if not Owner.validate_login(request.form):
        return redirect('/')
    
    query_data = {
        "email" : request.form["email"],
    }

    current_owner = Owner.get_owner_by_email(query_data)
    session["owner_id"] = current_owner.id
    return redirect ('/dashboard')

@app.route('/register', methods=['POST'])
def owner_register():
    if not Owner.validate_registration(request.form):
        return redirect('/')
    
    pass_hash = bcrypt.generate_password_hash(request.form["password"])

    query_data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "first_name" : request.form["first_name"],
        "password" : pass_hash
    }

    new_owner = Owner.create_owner(query_data)
    session["owner_id"] = new_owner
    return redirect ('/dashboard')

@app.route('/dashboard')
def home():
    if "owner_id" not in session:
        flash("Please login or register before entering site!")
        error = "error"
        return render_template("index.html", error = error)
    query_data = {
        'id' : session["owner_id"]
    }
    current_user = Owner.get_owner_by_ID(query_data)
    all_dogs = Dog.get_all_dogs()
    all_dogs_with_owners = Dog.get_dogs_and_owners()


    return render_template('/dashboard.html', current_user = current_user, all_dogs_with_owners = all_dogs_with_owners )

@app.route("/logout")
def logout():
    session.clear();
    return redirect("/")

