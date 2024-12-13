from flask import render_template, redirect, flash, request,session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFError
from pkg import app
from pkg.forms import Restaurantsignform, Restaurantlogform
from pkg.models import db, Restaurant, Farmer

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
    farmer_id = session.get("farmer_loggedin") 
    restaurant_id = session.get("restaurant_loggedin")

    farmer_deets = None
    rest_deets = None

    if farmer_id:
        farmer_deets = db.session.query(Farmer).get(farmer_id)
        print(farmer_deets)
    if restaurant_id:
        rest_deets = db.session.query(Restaurant).get(restaurant_id)
        print(rest_deets)

    return render_template('index.html', farmer_deets=farmer_deets, rest_deets=rest_deets)



# Route for the products page
@app.route('/products/')
def products():
    return render_template('user_restaurant/products.html')


# Route for the cart page
@app.route('/cart/')
def cart():
    return render_template('user_restaurant/cart.html/')

@app.route('/restaurant-signup/', methods=['GET', 'POST'])
def rest_signup():
    restaurant = Restaurantsignform()
    if request.method == 'GET':
        return render_template('user_restaurant/restaurant_signup.html', restaurant=restaurant)
    else:
        if restaurant.validate_on_submit():
            name = request.form.get('name')
            address = request.form.get('address')
            contact_email = request.form.get('contact_email')
            contact_num = request.form.get('contact_num')
            password = request.form.get('password')
            cpassword = request.form.get('cpassword')
            if password != cpassword:
                flash('Password mismatch, please try again', 'error')
                return redirect('/restaurant-signup/')
            else:
                hashed = generate_password_hash(password.strip())
                push_to_db = Restaurant(
                    rest_name=name,
                    rest_phone_number=contact_num,
                    rest_address=address,
                    rest_email=contact_email,
                    rest_password=hashed
                )
                db.session.add(push_to_db)
                db.session.commit()
                print(f"Hashed Password from DB: {hashed}")
                print(f"Plain Password: {password}")
                flash('An account has been created for you', 'success')
                return redirect('/restaurant-login/')
        else:
            for field, errors in restaurant.errors.items():
                for error in errors:
                    flash(f"Error in {field}: {error}", 'error')
    
    return render_template('user_restaurant/restaurant_signup.html', restaurant=restaurant)





@app.route('/restaurant-login/', methods=['GET', 'POST'])
def rest_login():
    restaurant = Restaurantlogform()
    if request.method == "GET":
        return render_template('user_restaurant/restaurant_login.html', restaurant=restaurant)
    else:
        if restaurant.validate_on_submit():
            email = restaurant.email.data
            password = restaurant.password.data
            print(f"Entered Password: {password}") 
            check_record = db.session.query(Restaurant).filter(Restaurant.rest_email == email).first()
            print(f"DB Record: {check_record}")  

            if check_record:
                hashed_password = check_record.rest_password
                print(f"Hashed Password from DB: {hashed_password}")  
                chk = check_password_hash(hashed_password.strip(), password.strip())
                print(f"Password Check Result: {chk}") 

                if chk:
                    session["restaurant_loggedin"] = check_record.rest_id
                    return redirect('/restaurant-dashboard/')
                else:
                    flash('Invalid Password', 'error')
                    return redirect('/restaurant-login/')
            else:
                flash('Invalid Email', 'error')
                return redirect('/restaurant-login/')
        else:
            for field, errors in restaurant.errors.items():
                for error in errors:
                    flash(f"Error in {field}: {error}", 'error')

    return render_template('user_restaurant/restaurant_login.html', restaurant=restaurant)

@app.route('/restaurant-dashboard/')
def restaurant_dashboard():
    restaurant_id = session.get("restaurant_loggedin")
    if restaurant_id:
        restaurant = db.session.query(Restaurant).filter(Restaurant.rest_id == restaurant_id).first()
        print(restaurant)
        if restaurant:
            restaurant_name = f"{restaurant.rest_name}"
            return render_template('user_restaurant/restaurant_dashboard.html', restaurant_name=restaurant_name)
        flash('errors', 'You need to log in first!')
        return redirect('/restaurant-login/')
    return render_template('user_restaurant/restaurant_dashboard.html')

@app.route("/restaurant-logout/")
def restaurant_logout():
    session.pop('restaurant_loggedin', None)
    return redirect('/')
