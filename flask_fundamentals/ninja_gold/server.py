from flask import Flask, render_template, request, redirect, session
import random
app = Flask(__name__)
app.secret_key = "secret ninja gold"

@app.route('/', methods= ['GET', 'POST'])
def index():
    
    if 'gold' not in session:
        session['gold'] = 0
    else:
        session['gold'] = session['gold']
    
    
    return render_template('index.html')

@app.route('/process_money', methods = ['GET', 'POST'])
def process_money():
    
    if 'gold' not in session:
        session['gold'] = 0
    if 'activity' not in session:
        session['activity'] = []
    print(session['activity']) 
    
    
    if request.form['id']=='farm':
        print(request.form['id'])
        session['farm'] = random.randrange(10, 21)
        session['gold'] += session['farm']
        session['activity'].insert(0, f"<p style='color: green'>Earned {session['farm']} golds from the farm!</p>")

    if request.form['id']=='cave':
        print(request.form['id'])
        session['cave'] = random.randrange(5, 11)
        session['gold'] += session['cave']
        session['activity'].insert(0, f"<p style='color: green'>Earned {session['cave']} golds from the cave!</p>")

    if request.form['id']=='house':
        print(request.form['id'])
        session['house'] = random.randrange(2, 6)
        session['gold'] += session['house']
        session['activity'].insert(0, f"<p style='color: green'>Earned {session['house']} golds from the house!</p>")

    if request.form['id']=='casino':
        print(request.form['id'])
        session['casino'] = random.randrange(-50, 50)
        session['gold'] += session['casino']
        if session['casino'] > 0:
            session['activity'].insert(0, f"<p style='color: green'>Earned {session['casino']} golds from the casino!</p>")
        elif session['casino'] < 0:
            session['activity'].insert(0, f"<p style='color: red'>Earned a casino and lost {session['casino']} golds... Ouch =(</p>")
        else:
            session['activity'].insert(0, f"<p style='color: blue'>Earned a casino and get/lost {session['casino']} golds</p>")
    
    print(session['gold'])  
    print(session['activity'])
    return redirect('/')
@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')
    
if __name__ == "__main__":
    app.run(debug=True)