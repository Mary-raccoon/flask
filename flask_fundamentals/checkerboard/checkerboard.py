from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", x = 8, y = 8, color1 = "aqua", color2 = "pink")

@app.route('/<x>')
def repeat(x):
    return render_template("index.html", x = int(x), y = int(x), color1 = "aqua", color2 = "pink")

@app.route('/<x>/<y>')
def row_colomn(x, y):
    return render_template("index.html", x = int(x), y = int(y), color1 = "aqua", color2 = "pink")

@app.route('/<x>/<y>/<color1>/<color2>')
def colors(x, y, color1, color2):
    return render_template("index.html", x = int(x), y = int(y), color1 = color1, color2 = color2)

if __name__=="__main__":
    app.run(debug=True)

