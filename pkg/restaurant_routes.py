from flask import render_template, redirect, flash, request, url_for
from flask_wtf.csrf import CSRFError
from pkg import app
from pkg.forms import Restaurantsignform, Restaurantlogform

@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response


@app.errorhandler(CSRFError)
def handle_csrf(e):
    return render_template('csrf_error.html', reason=e.description)

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')


# Route for the products page
@app.route('/products/')
def products():
    return render_template('user_restaurant/products.html')



# Route for the cart page
@app.route('/cart/')
def cart():
    return render_template('user_restaurant/cart.html/')



# Route for the restaurant dashboard
@app.route('/restaurant-dashboard/')
def restaurant_dashboard():
    return render_template('user_restaurant/restaurant-dashboard.html')

# Route for the login page
# @app.route('/login/', methods=['GET','POST'])
# def login():
#     farmer = Farmerform()
#     restaurant = Restaurantform()
#     if farmer.validate_on_submit():
#         email = farmer.email.data
#         password = farmer.password.title
#         # return redirect('/farmer_dashboard/')
#         return f'{email}{password}'
#     elif restaurant.validate_on_submit():
#         email = restaurant.email.data
#         password = restaurant.password.title
#         return redirect('/restaurant_dashboard/')
#     return render_template('login.html', farmer=farmer, restaurant=restaurant)

@app.route('/restaurant-login/', methods=['GET', 'POST'])
def rest_login(): 
    restaurant = Restaurantlogform()
    return render_template('user_restaurant/restaurant_login.html',restaurant=restaurant)


@app.route('/restaurant-signup/',methods=['GET', 'POST'])
def rest_signup(): 
    restaurant = Restaurantsignform()
    return render_template('user_restaurant/restaurant_signup.html',restaurant=restaurant)
