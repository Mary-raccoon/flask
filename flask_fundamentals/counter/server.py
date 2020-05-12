from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = 'secret counter'

@app.route('/')
def index():
    if 'counter' not in session:
        session['counter'] = 0
    else:
        session ['counter'] += 1
    return render_template("index.html", counter=session['counter'])

@app.route('/destroy_session', methods=['POST'])
def destroy():
    session['counter'] = 0
    return redirect('/')

@app.route('/plus_two', methods=['POST'])
def plus_two():
    session['counter'] += 1
    return redirect('/')

@app.route('/plus/<x>')
def plus_x(x):
    session['counter'] += int(x)-1
    return redirect('/')

@app.route('/plus_y', methods=['POST'])
def plus_y():
    session['y'] = request.form['num']
    if session['y']:
        session['counter'] += int(session['y'])-1
    else:
        session['counter'] -= 1
    return redirect('/')
if __name__== "__main__":
    app.run(debug=True)