from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
import re 
from flask_bcrypt import Bcrypt 

app = Flask(__name__)
bcrypt = Bcrypt(app) 
app.secret_key = 'secret log_reg'
mysql = connectToMySQL("log_reg")

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/success')
def success():
    if len(session) == 0:
        flash("You must be logged in to enter this website", "none")
        return redirect('/')
    return render_template("success.html")

@app.route('/register', methods=['POST'])
def register():
    first = request.form['f_name']
    last = request.form['l_name']
    email = request.form['email']
    passw = request.form['password']
    conf = request.form['confirm']

    
    errors = False
    if len(first) < 1:
        flash("This field is required!",'f_name')
        errors = True
    elif len(first) < 3 or not NAME_REGEX.match(first):
        flash("First name mast contain atleast two letters and only letters", 'f_name')
        errors = True

    if len(last) < 1:
        flash("This field is required!", 'l_name')
        errors = True
    elif len(last) < 3 or not NAME_REGEX.match(last):      
        flash("Last name mast contain atleast two letters and only letters", 'l_name')
        errors = True

    if len(email) < 1:
        flash("This field is required!", 'email')
        errors = True
    elif not EMAIL_REGEX.match(email):
        flash("Invalid Email Address!", 'email')
        errors = True
    else:
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = {"email": email}
        result = mysql.query_db(query, data)
        if result:
            flash("This email is already taken!", 'email')
            errors = True

    if len(passw) < 1:
        flash("This field is required!", 'password')
        errors = True
    elif len(passw) < 8 or len(passw) > 15:         
        flash("Password must be between 8 and 15 characters", 'password') 
        errors = True

    if len(conf) < 1:
        flash("This field is required!", 'confirm')
        errors = True
    elif conf != passw:
        flash("Passwords must match", 'confirm')
        errors = True

    if errors:
        print("f_name:", first)
        return redirect("/")

    else:
        session['f_name'] = first
        pw_hash = bcrypt.generate_password_hash(passw)  
        print(pw_hash) 
        query = "INSERT INTO users (f_name, l_name, email, password, created_at, updated_at) VALUES (%(f_name)s, %(l_name)s, %(email)s, %(password_hash)s,NOW(), NOW());"
        data = {
            "f_name": first,
            "l_name": last,
            "email": email,
            "password_hash": pw_hash
            }
        mysql.query_db(query, data)
        flash("You've been seccessfully registered!")
        return redirect('/success')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email_log']
    passw = request.form['password_log']
    
    if len(email) > 0 and len(passw) > 0:
        query = "SELECT * FROM users WHERE email = %(email)s"
        data = { "email": email}
        result = mysql.query_db(query, data)
        
        if len(result) > 0:
            if bcrypt.check_password_hash(result[0]['password'], passw):
                session['id'] = result[0]['id']
                session['f_name'] = result[0]['f_name']
                flash("You've been seccessfully logged in!")
                return redirect('/success')
            else: 
                flash("You could not be logged in", "fail")
                return redirect('/')
        
    flash("You could not be logged in", "fail")
    return redirect('/')

@app.route('/logout')
def logout():
    flash("You've been logged out", "none")
    session.clear()
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)