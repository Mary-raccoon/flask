from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = 'secret user'
@app.route('/')
def index():
    mysql = connectToMySQL("first_flask")
    friends = mysql.query_db("SELECT * FROM friends;") 
    print(friends)
    return render_template("index.html", all_friends = friends)
  
@app.route('/process', methods=['POST'])
def add_friend_to_db():
    mysql = connectToMySQL("first_flask")
    if len(request.form['fname']) < 1:
    	flash("Please enter a first name")
    if len(request.form['lname']) < 1:
    	flash("Please enter a last name")
    if len(request.form['occ']) < 2:
    	flash("Occupation should be at least 2 characters")
    
    if not '_flashes' in session.keys():
        
        query = "INSERT INTO friends(first_name, last_name, occupation, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(occup)s, NOW(), NOW());"
        data = {
            "fn": request.form["fname"],
            "ln": request.form["lname"],
            "occup": request.form["occ"],
        }
        new_friend_id = mysql.query_db(query, data)
        flash("Friend successfully added!")
    return redirect('/') # either way the application should return to the index and display the message

if __name__=="__main__":
    app.run(debug=True)
