from flask import Flask, render_template, redirect, request, flash, session
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = "secret dojo"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/result')
def result():
    mysql = connectToMySQL('dojo_survey')
    ninjas = mysql.query_db("SELECT * FROM ninjas;") 
    return render_template("result.html", ninjas=ninjas)

@app.route('/result', methods=['POST'])
def create():
    mysql = connectToMySQL('dojo_survey')
    if len(request.form['full_name']) < 1:
        flash("Please enter your name")
    if len(request.form['language']) < 1:
        flash("Please choose your favorite language")
    if len(request.form['location']) < 1:
        flash("Please choose your location")
    if len(request.form['comment']) < 4:
        flash("Your comment shoul be longer then 3 char")
        
    if '_flashes' in session.keys():
        return redirect('/')
    else:
        query = "INSERT INTO ninjas (full_name, language, location, comment, created_at, updated_at) VALUES (%(full_name)s, %(language)s, %(location)s, %(comment)s, NOW(), NOW());"
        data = {
            "full_name": request.form['full_name'],
            "comment": request.form['comment'], 
            "language": request.form['language'],
            "location": request.form['location']
        }
        new_ninja = mysql.query_db(query, data)

        session['full_name'] = request.form['full_name']
        session['comment'] = request.form['comment']
        session['language'] = request.form['language']
        session["location"] = request.form['location']
        return redirect("/result")

if __name__=="__main__":
    app.run(debug=True)
