from flask import Flask, render_template, redirect, request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/result', methods=['POST'])
def result():
    print("Got Post Info")
    print(request.form)
    info = {
        "name": request.form['name'],
        "location": request.form['location'],
        "language": request.form['language'],
        "comment": request.form['comment']
    }
    return render_template("result.html", info=info)

if __name__=="__main__":
    app.run(debug=True)
