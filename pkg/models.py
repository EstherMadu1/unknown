from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class State(db.Model):
    __tablename__ = 'states'
    state_id = db.Column(db.Integer, primary_key=True)
    state_name = db.Column(db.String(15), nullable=False)

class Farmer(db.Model):
    __tablename__ = 'farmers'
    farm_id = db.Column(db.Integer, primary_key=True)
    farm_name = db.Column(db.String(50), nullable=False)
    farmer_first_name = db.Column(db.String(45), nullable=False)
    farmer_last_name = db.Column(db.String(45), nullable=False)
    farmer_phone_number = db.Column(db.String(20), nullable=False)
    farmer_email = db.Column(db.String(20), nullable=False)
    farmer_state_id = db.Column(db.Integer, db.ForeignKey('states.state_id'), nullable=False)
    farmer_address = db.Column(db.Text, nullable=False)
    farmer_username = db.Column(db.String(20), unique=True, nullable=False)
    farmer_password = db.Column(db.String(20), nullable=False)
    date_registered = db.Column(db.DateTime(), default=datetime.utcnow)

class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(25), nullable=False)

class Product(db.Model):
    __tablename__ = 'products'
    pro_id = db.Column(db.Integer, primary_key=True)
    pro_name = db.Column(db.String(300), nullable=False)
    pro_category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=False)
    qua_avail = db.Column(db.Float, nullable=False)
    price_per_unit = db.Column(db.Numeric(10, 2), nullable=False)
    farm_id = db.Column(db.Integer, db.ForeignKey('farmers.farm_id'), nullable=False)
    pro_picture = db.Column(db.LargeBinary)
    pro_status = db.Column(db.String(45), nullable=False)

class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    rest_id = db.Column(db.Integer, primary_key=True)
    rest_name = db.Column(db.String(40), nullable=False)
    rest_phone_number = db.Column(db.String(20), nullable=False)
    rest_address = db.Column(db.Text, nullable=False)
    rest_email = db.Column(db.String(45), nullable=False)
    rest_password = db.Column(db.String(45), nullable=False)
    date_registered = db.Column(db.DateTime, nullable=False)

class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.rest_id'), nullable=False)
    order_date = db.Column(db.DateTime(), default=datetime.utcnow)
    total_amt = db.Column(db.Numeric(10, 2), nullable=False)
    order_stat = db.Column(db.String(45), nullable=False)

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    order_item_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    pro_id = db.Column(db.Integer, db.ForeignKey('products.pro_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class Payment(db.Model):
    __tablename__ = 'payments'
    pay_id = db.Column(db.Integer, primary_key=True)
    pay_order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    pay_amt = db.Column(db.String(45), nullable=False)
    pay_status = db.Column(db.String(45), nullable=False)
    reference_num = db.Column(db.String(45), nullable=False)
    date_paid = db.Column(db.DateTime(), default=datetime.utcnow)

class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True)
    admin_username = db.Column(db.String(75), unique=True, nullable=False)
    admin_password = db.Column(db.String(45), nullable=False)
    admin_last_login = db.Column(db.DateTime, nullable=False)
