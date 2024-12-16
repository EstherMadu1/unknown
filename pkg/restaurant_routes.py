from flask import current_app as app
from flask import render_template, redirect, flash, request, session
from flask_wtf.csrf import CSRFError
from werkzeug.security import generate_password_hash, check_password_hash

from pkg.forms import Restaurantsignform, Restaurantlogform
from pkg.models import db, Restaurant, Farmer, Product, Category, CartItem, Order, OrderItem, Admin


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
    admin_id = adminn_id = session.get("admin_loggedin")

    farmer_deets = None
    rest_deets = None
    admin_deets = None

    if farmer_id:
        farmer_deets = db.session.query(Farmer).get(farmer_id)
        
    if restaurant_id:
        rest_deets = db.session.query(Restaurant).get(restaurant_id)
    
    if admin_id:
        admin_deets = db.session.query(Admin).get(admin_id)

    return render_template('index.html', farmer_deets=farmer_deets, rest_deets=rest_deets, admin_deets=admin_deets)



# Route for the products page
@app.route('/products/', methods=['GET'])
def products():
    product_name = request.args.get('product_name')  # Get the query parameter for product_name

    if product_name:
        category = Category.query.filter_by(category_name=product_name).first()
        products_ = db.session.query(Product).filter(
            Product.pro_category_id == category.category_id
        ).all() if category else []
    else:
        products_ = db.session.query(Product).all()

    cart_items = []
    if 'restaurant_loggedin' in session:
        restaurant_id = session['restaurant_loggedin']
        user_cart_items = db.session.query(CartItem).filter_by(restaurant_id=restaurant_id).all()
        for item in user_cart_items:
            product = db.session.query(Product).filter_by(pro_id=item.pro_id).first()
            if product:
                cart_items.append({
                    'pro_id': item.pro_id,
                    'cart_item_id': item.cart_item_id,
                    'product_name': product.pro_name,
                    'quantity': item.cart_quantity,
                    'price_per_unit': float(product.price_per_unit),
                    'total_price': float(item.cart_quantity * product.price_per_unit)
                })

    return render_template('user_restaurant/products.html', products=products_, cart_items=cart_items)


# Route for the cart page
@app.route('/cart/', methods=['GET'])
def get_cart():
    if 'restaurant_loggedin' not in session:
        flash('You need to log in to view your cart!', 'error')
        return redirect('/restaurant-login/')

    restaurant_id = session['restaurant_loggedin']
    cart_items = db.session.query(CartItem).filter_by(restaurant_id=restaurant_id).all()

    cart_details = []
    for item in cart_items:
        product = db.session.query(Product).filter_by(pro_id=item.pro_id).first()
        if product:
            cart_details.append({
                'pro_id': item.pro_id,
                'pro_picture': product.pro_picture,
                'cart_item_id': item.cart_item_id,
                'product_name': product.pro_name,
                'quantity': item.cart_quantity,
                'price_per_unit': float(product.price_per_unit),
                'total_price': float(item.cart_quantity * product.price_per_unit)
            })

    return render_template('user_restaurant/cart.html', cart_items=cart_details)


@app.route('/cart/add/', methods=['POST'])
def add_to_cart():
    if 'restaurant_loggedin' not in session:
        flash('You need to log in to add items to the cart!', 'error')
        return redirect('/restaurant-login/')

    restaurant_id = session['restaurant_loggedin']
    pro_id = request.form.get('pro_id')
    quantity = request.form.get('quantity', type=int)

    if not pro_id or quantity <= 0:
        flash('Invalid product or quantity', 'error')
        return redirect('/products/')

    existing_cart_item = db.session.query(CartItem).filter_by(pro_id=pro_id, restaurant_id=restaurant_id).first()

    if existing_cart_item:
        existing_cart_item.cart_quantity += quantity
    else:
        new_cart_item = CartItem(
            pro_id=pro_id,
            cart_quantity=quantity,
            restaurant_id=restaurant_id
        )
        db.session.add(new_cart_item)

    db.session.commit()
    flash('Item added to cart!', 'success')
    return redirect('/cart/')


@app.route('/cart/update/<int:cart_item_id>/', methods=['POST'])
def update_cart(cart_item_id):
    if 'restaurant_loggedin' not in session:
        flash('You need to log in to update the cart!', 'error')
        return redirect('/restaurant-login/')

    quantity = request.form.get('quantity', type=int)

    if quantity <= 0:
        flash('Invalid quantity!', 'error')
        return redirect('/cart/')

    cart_item = db.session.query(CartItem).filter_by(cart_item_id=cart_item_id).first()

    if cart_item:
        cart_item.cart_quantity = quantity
        db.session.commit()
        flash('Cart item updated!', 'success')
    else:
        flash('Cart item not found!', 'error')

    return redirect('/cart/')


@app.route('/cart/remove/<int:cart_item_id>/', methods=['POST'])
def remove_from_cart(cart_item_id):
    if 'restaurant_loggedin' not in session:
        flash('You need to log in to remove items from the cart!', 'error')
        return redirect('/restaurant-login/')

    cart_item = db.session.query(CartItem).filter_by(cart_item_id=cart_item_id).first()

    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed from cart!', 'success')
    else:
        flash('Cart item not found!', 'error')

    return redirect('/cart/')


@app.route('/checkout/', methods=['POST'])
def checkout():
    if 'restaurant_loggedin' not in session:
        flash('You need to log in to proceed with checkout!', 'error')
        return redirect('/restaurant-login/')

    restaurant_id = session['restaurant_loggedin']
    cart_items = db.session.query(CartItem).filter_by(restaurant_id=restaurant_id).all()

    if not cart_items:
        flash('Your cart is empty!', 'error')
        return redirect('/cart/')

    total_amt = sum(
        item.cart_quantity * db.session.query(Product.price_per_unit).filter_by(pro_id=item.pro_id).scalar()
        for item in cart_items
    )

    new_order = Order(
        restaurant_id=restaurant_id,
        total_amt=total_amt,
        order_stat='Pending'
    )
    db.session.add(new_order)
    db.session.commit()

    for item in cart_items:
        order_item = OrderItem(
            order_id=new_order.order_id,
            pro_id=item.pro_id,
            quantity=item.cart_quantity
        )
        db.session.add(order_item)
        db.session.delete(item)

    db.session.commit()

    flash('Order placed successfully!', 'success')
    return redirect('/restaurant-dashboard/')



# @app.route('/delivered-orders/')
# def restaurant_orders():
#     restaurant_id = session.get("restaurant_loggedin")
    
#     if not restaurant_id
#     restaurant = Restaurant.query.get(restaurant_id)
#     for order in restaurant.orders:
#         print(f"Order ID: {order.order_id}, Date: {order.order_date}, Status: {order.order_stat}")
#     for item in order.order_items:
#         print(f"  Product: {item.product.pro_name}, Category: {item.product.category.category_name}, Quantity: {item.quantity}")
#     return 'check'
    
    

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


@app.route("/restaurant-logout/")
def restaurant_logout():
    session.pop('restaurant_loggedin', None)
    return redirect('/')

