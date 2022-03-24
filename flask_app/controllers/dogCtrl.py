from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.dog import Dog
from flask_app.models.owner import Owner
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not "owner_id" in session:
            flash("Access Denied: Login Required")
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/dog/info/<int:dog_id>')
def view_dog(dog_id):
    if "owner_id" not in session:
        flash("Please login or register before entering site!")
        return redirect("/")
    one_dog = Dog.get_dog_by_ID(dog_id)
    return render_template("dogInfo.html", one_dog = one_dog)

#------------------- create --------------------

@app.route('/dog/create/')
@login_required
def create_dog():
    return render_template("dogForm.html")
    
@app.route('/dog/create/confirm', methods = ['POST'])
@login_required
def create_dog_confirm():
    # if "owner_id" not in session:
    #     flash("Please login or register before entering site!")
    #     return redirect("/")

    query_data = {
        'name' : request.form['name'],
        'breed' : request.form['breed'],
        'age' : request.form['age'],
        'owner_id' : session['owner_id']
    }
    Dog.create_dog(query_data)
    return redirect('/dashboard')
    

#------------------- edit --------------------

@app.route('/dog/edit/<int:dog_id>')
@login_required
def edit_dog(dog_id):
    # if "owner_id" not in session:
    #     flash("Please login or register before entering site!")
    #     return redirect("/")

    query_data = {
        "id" : dog_id
    }
    one_dog = Dog.get_dog_by_ID(query_data)
    if session["owner_id"] != one_dog.owner.id:
        flash("This is not your dog!")
        return redirect("/dashboard")
    return render_template("dogForm.html", one_dog = one_dog, edit = True)

@app.route('/dog/edit/confirm/<int:dog_id>', methods = ['POST'])
@login_required
def edit_dog_confirm(dog_id):
    # if "owner_id" not in session:
    #     flash("Please login or register before entering site!")
    #     return redirect("/")
    query_data = {
        'id' : dog_id,
        'name' : request.form['name'],
        'breed' : request.form['breed'],
        'age' : request.form['age']
    }
    one_dog = Dog.get_dog_by_ID(query_data)
    if session["owner_id"] != one_dog.owner.id:
        flash("This is not your dog!")
        return redirect("/dashboard")
    Dog.edit_dog(query_data)
    return redirect('/dashboard')

#------------------- delete --------------------

@app.route('/dog/delete/confirm/<int:dog_id>')
@login_required
def delete_dog_confirm(dog_id):
    # if "owner_id" not in session:
    #     flash("Please login or register before entering site!")
    #     return redirect("/")
    query_data = {
        'id' : dog_id
    }
    one_dog = Dog.get_dog_by_ID(query_data)
    if session["owner_id"] != one_dog.owner.id:
        flash("This is not your dog!")
        return redirect("/dashboard")
    Dog.delete_dog(query_data)
    return redirect('/dashboard')


