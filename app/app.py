from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/candy'
db = SQLAlchemy(app)

class Candy(db.Model):
    __tablename__ = "candies"
    id = db.Column(db.Integer, primary_key=True)
    competitorname = db.Column(db.String(120), unique=True)
    chocolate = db.Column(db.Integer())
    fruity = db.Column(db.Integer())
    caramel = db.Column(db.Integer())
    peanutyalmondy = db.Column(db.Integer())
    nougat = db.Column(db.Integer())
    crispedricewafer = db.Column(db.Integer())
    hard = db.Column(db.Integer())
    bar = db.Column(db.Integer())
    pluribus = db.Column(db.Integer())
    sugarpercent = db.Column(db.Float())
    pricepercent = db.Column(db.Float())
    winpercent = db.Column(db.Float())

    def display_json():
        return [{
            "name": candy.competitorname,
            "winpercent": candy.winpercent
        } for candy in Candy.query.all()]


@app.route('/')
def show_candies():
    candies = Candy.query.all()
    return render_template('candy_list.html', candies=candies, candy_json=Candy.display_json())

if __name__ == '__main__':
    app.debug = True
    app.run()
