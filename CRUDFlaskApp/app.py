

from flask import Flask, render_template, request, redirect, session, url_for

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///customer.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "secretkey"

db = SQLAlchemy(app)

class customer(db.Model):
    cust_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40))
    gender = db.Column(db.String(15))
    age = db.Column(db.Integer)
    mail = db.Column(db.String(25))

    def __init__(self, cust_id, name, gender, age, mail) -> None:
        self.cust_id = cust_id
        self.gender = gender
        self.age = age
        self.name = name
        self.mail = mail

    def __repr__(self) -> str:
        return f'{self.cust_id} - {self.name} - {self.age}'



@app.route('/')
def display():
    return render_template('index.html', customers = customer.query.all())

@app.route('/adduser', methods = ['GET', 'POST'])
def adduser():
    if request.method == 'POST':
        cust_id = request.form["cust_id"]
        name = request.form["name"]
        gender = request.form["gender"]
        age = int(request.form["age"])
        mail = request.form["mail"]
        data = customer(cust_id, name, gender, age, mail)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('display'))
    return render_template('adduser.html')

@app.route('/deluser', methods = ['POST', 'GET'])
def deluser():
    if request.method == 'POST':
        cust_id = request.form['cust_id']
        cust = customer.query.get(cust_id)
        db.session.delete(cust)
        db.session.commit()
        return redirect(url_for('display'))
    return render_template('deluser.html')


@app.route('/updateuser', methods = ["POST", "GET"])
def updateuser():
    if request.method == "POST":
        cust_id = request.form['cust_id']
        cust = customer.query.get(cust_id)
        name = request.form["name"]
        gender = request.form["gender"]
        age = int(request.form["age"])
        mail = request.form["mail"]
        cust.name = name
        cust.gender = gender
        cust.age = age
        cust.mail = mail
        db.session.commit()
        return redirect(url_for('display'))
    return render_template('updateuser.html')

        









if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)
