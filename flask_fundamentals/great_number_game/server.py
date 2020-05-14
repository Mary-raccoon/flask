from flask import Flask, render_template, request, redirect, session
import random 	

app = Flask(__name__)
app.secret_key = "Secret number"

@app.route('/')
def index():
    
    info = {
        "message": None,
        "css_class": None
    }

    if 'random' not in session:
        session['random'] = random.randint(1,100)
    if "count" not in session:
        session['count'] = 0
    if "guess" not in session:
        info["message"] = ""
        info['css_class'] = "yellow"
    elif int(session['count']) > 4:
        info["message"] = "You lose!"
        info["css_class"] = "red"
    elif int(session["guess"] )> int(session["random"]):
        info["message"] = "Too high!"
        info['css_class'] = "red"
    elif int(session["guess"]) < int(session["random"]):
        info["message"] = "Too low!"
        info['css_class'] = "red"
    else:
        info["message"] = f"{session['random']} was the number!"
        info['css_class'] = "green"
    
    return render_template('index.html',info = info)
    

@app.route('/guess', methods=['POST'])
def guess():
    session['guess'] = request.form['guessed_number']    
    session['count'] += 1
    return redirect("/")

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    session.clear()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)