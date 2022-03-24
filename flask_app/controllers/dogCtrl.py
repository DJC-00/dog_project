from flask_app import app
from flask import render_template,redirect,request,session
from flask_app.models.dog import Dog
from flask_app.models.owner import Owner

@app.route('/dog/info/<int:dog_id>')
def view_dog(dog_id):
    one_dog = Dog.get_dog_by_ID(dog_id)
    return render_template("dogInfo.html", one_dog = one_dog)

#------------------- create --------------------

@app.route('/dog/create/')
def create_dog():
    return render_template("dogForm.html")
    
@app.route('/dog/create/confirm', methods = ['POST'])
def create_dog_confirm():
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
def edit_dog(dog_id):
    query_data = {
        "id" : dog_id
    }
    one_dog = Dog.get_dog_by_ID(query_data)
    return render_template("dogForm.html", one_dog = one_dog, edit = True)

@app.route('/dog/edit/confirm/<int:dog_id>', methods = ['POST'])
def edit_dog_confirm(dog_id):
    query_data = {
        'id' : dog_id,
        'name' : request.form['name'],
        'breed' : request.form['breed'],
        'age' : request.form['age']
    }
    Dog.edit_dog(query_data)
    return redirect('/dashboard')

#------------------- delete --------------------

@app.route('/dog/delete/confirm/<int:dog_id>')
def delete_dog_confirm(dog_id):
    query_data = {
        'id' : dog_id
    }
    Dog.delete_dog(query_data)
    return redirect('/dashboard')