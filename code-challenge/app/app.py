#!/usr/bin/env python3

from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate

from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''

@app.route('/restaurants', methods=['GET'])
def restaurants():
    restaurants = Restaurant.query.all()
    rest_dicts = [r.to_dict() for r in restaurants]
    return make_response(jsonify(rest_dicts), 200)

@app.route('/restaurants/<int:id>', methods=['GET'])
def restaurant_by_id(id):
    rest = Restaurant.query.get(id)
    return make_response(jsonify(rest.to_dict()), 200)

@app.route('/pizzas')
def pizzas():
    return ''

@app.route('/restaurant_pizzas')
def resaurant_pizzas():
    return ''


if __name__ == '__main__':
    app.run(port=3000)
