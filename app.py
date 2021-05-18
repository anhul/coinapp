from flask import Flask
from flask import jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coin_catalog.db'
db = SQLAlchemy(app)


class Coin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    denomination = db.Column(db.String(30))
    year = db.Column(db.Integer)

    def __repr__(self):
        return f'{self.denomination } {self.year} {self.country.name}'


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    # Refers to the Coin class to get a list of coin objects belonging to country
    # Adds implicitly country property to Coin class, country is object of class Country
    coins = db.relationship('Coin', backref='country', lazy=True)

    def __repr__(self):
        return f'{self.name}'

@app.route('/countries')
def get_countries():
    return jsonify([{'name': country.name} for country in Country.query.all()])


@app.route('/countries', methods=['POST'])
def add_country():
    country = Country(name=request.json['name'])
    db.session.add(country)
    db.session.commit()
    return jsonify({'id': country.id})

@app.route('/countries/<id>', methods=['DELETE'])
def delete_country(id):
    country = Country.query.get(id)
    if country is None:
        return jsonify({'message': 'error: country not found'})
    db.session.delete(country)
    db.session.commit()
    return jsonify({'message': 'success'})

