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

@app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
def restaurant_by_id(id):
    rest = Restaurant.query.get(id)

    if rest is None:
        return make_response(jsonify({'error': 'Restaurant not found'}), 404)

    if request.method == 'GET':
        return make_response(jsonify(rest.to_dict()), 200)
    
    elif request.method == 'DELETE':
        rps = RestaurantPizza.query.filter(
            RestaurantPizza.restaurant_id == rest.id
        ).all()
        for row in rps:
            db.session.delete(row)
        db.session.delete(rest)
        db.session.commit()
        return make_response(jsonify({}), 200)

@app.route('/pizzas')
def pizzas():
    pizzas = Pizza.query.all()
    pizzas_dict = [pizza.to_dict() for pizza in pizzas]
    return make_response(jsonify(pizzas_dict), 200)

@app.route('/pizzas/<int:id>', methods=['PATCH'])
def pizza_by_id(id):
    pizza = Pizza.query.filter(Pizza.id == id).first()
    body = request.get_json()
    # can update fields all at once:
    for field, value in body.items():
        setattr(pizza, field, value)
    # or one by one:
    # if 'name' in body:
    #     pizza.name = body.get('name')
    # if 'ingredients' in body:
    #     pizza.ingredients = body.get('ingredients')
    db.session.add(pizza)
    db.session.commit()
    return make_response(jsonify(pizza.to_dict()), 200)

@app.route('/restaurant_pizzas', methods=['POST'])
def resaurant_pizzas():
    body = request.get_json()
    try:
        new_rp = RestaurantPizza(
            price=body.get('price'),
            restaurant_id=body.get('restaurant_id'),
            pizza_id=body.get('pizza_id')
        )
    except ValueError:
        return make_response(jsonify({'errors': ['validation errors']}), 404)
    db.session.add(new_rp)
    db.session.commit()
    # pizza = Pizza.query.filter(Pizza.id == body['pizza_id']).first()
    pizza = new_rp.pizza
    return make_response(jsonify(pizza.to_dict()), 201)


if __name__ == '__main__':
    app.run(port=3000)
