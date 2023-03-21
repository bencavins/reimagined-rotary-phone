from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    restaurant_pizzas = db.relationship('RestaurantPizza', backref='restaurant')

    def to_dict(self):
        pizzas = [rp.pizza for rp in self.restaurant_pizzas]
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'pizzas': [pizza.to_dict() for pizza in pizzas]
            # 'pizzas': [rp.pizza.to_dict() for rp in self.restaurant_pizzas]
        }

class Pizza(db.Model):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())

    restaurant_pizzas = db.relationship('RestaurantPizza', backref='pizza')

    def to_dict(self):
        return {
            'id': self.id,
            'ingredients': self.ingredients,
            'name': self.name
        }

class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())

    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))

    @validates('price')
    def validate_price(self, key, new_price):
        if new_price < 1 or new_price > 30:
            raise ValueError(f'Invalid price: {new_price}')
        else:
            return new_price