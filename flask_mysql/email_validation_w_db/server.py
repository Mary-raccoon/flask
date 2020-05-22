from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
import re 

app = Flask(__name__)
app.secret_key = 'secret email'
mysql = connectToMySQL("email_validation")
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/create', methods=["POST"])
def create():
    if len(request.form['email']) < 1:
        flash("Email can't be blank!")
        return redirect('/') 
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!")
        return redirect('/') 

    else:
        query = "SELECT * FROM emails WHERE email = %(email)s;"
        data = {"email": request.form['email']}
        result = mysql.query_db(query, data)
        if result:
            flash("This email is already taken!")
            return redirect("/") 
        else:
            query = "INSERT INTO emails (email, created_at, updated_at) VALUES (%(email)s, NOW(), NOW());"
            data = {"email": request.form['email']}
            mysql.query_db(query, data)
            flash(f"The email address you intered {request.form['email']} is a VALID email address! Thank you!")
            return redirect('/success')

@app.route('/success')
def success():
    all_emails = mysql.query_db("SELECT * FROM emails")
    print(all_emails)
    return render_template("success.html", all_emails=all_emails)

@app.route('/<id>/destroy')
def delete_user(id):
    query = "DELETE FROM emails WHERE id = %(id)s;"
    data = {'id': id}
    mysql.query_db(query, data)
    return redirect('/success')

if __name__=="__main__":
    app.run(debug=True)