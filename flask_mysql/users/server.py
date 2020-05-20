from flask import Flask, render_template, redirect, request
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = 'secret user'

@app.route('/users')
def index():
    mysql = connectToMySQL('users')
    all_users = mysql.query_db("SELECT * FROM users.friends;")
    return render_template("index.html", all_users = all_users)

@app.route('/users/new')
def new():
    return render_template("new.html")

@app.route('/create_user', methods=["POST"])
def create():
    mysql = connectToMySQL('users')
    query = "INSERT INTO users.friends (first_name, last_name, email, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, NOW(), NOW());"
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email']
    }
    new_user = mysql.query_db(query, data)    
    return redirect("/users/new")

@app.route('/users/<id>')
def show(id):
    mysql = connectToMySQL('users')
    query = "SELECT friend_id, CONCAT(first_name, ' ', last_name) AS full_name, email, created_at, updated_at FROM users.friends WHERE friend_id = %(id)s;"
    data = {"id": id}
    users = mysql.query_db(query, data)
    print("user id:", id)
    return render_template('show.html', users = users)

@app.route('/users/<id>/edit')
def edit(id):
    mysql = connectToMySQL('users')
    query = "SELECT * FROM users.friends WHERE friend_id = %(id)s;"
    data = {"id": id}
    users = mysql.query_db(query, data)
    print("user:", users)
    return render_template('edit.html', users = users)

@app.route('/users/<id>/update', methods=["POST"])
def update(id):
    mysql = connectToMySQL('users')
    query = "UPDATE users.friends SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at = NOW() WHERE friend_id = %(id)s;"
    data = {
        "id": id,
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email']
    }
    user_id = mysql.query_db(query, data)
    print("updated_user:", user_id)
    return redirect('/users/'+id)

@app.route('/users/<id>/destroy')
def delete_user(id):
    mysql = connectToMySQL('users')
    query = "DELETE FROM users.friends WHERE friend_id = %(id)s;"
    data = {
        'id': id
    }
    mysql.query_db(query, data)
    return redirect('/users')

if __name__ == "__main__":
    app.run(debug=True)