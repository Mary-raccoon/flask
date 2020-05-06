from flask import Flask, render_template  
app = Flask(__name__) 

@app.route('/play')
def index():
    return render_template("index.html", color = "aqua")

@app.route('/play/<x>')
def repeat(x):
    return render_template("index.html", x=int(x), color = "aqua")

if __name__=="__main__":
    app.run(debug=True)  