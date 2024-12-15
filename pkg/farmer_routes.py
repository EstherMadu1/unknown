from flask import render_template, redirect, flash, request, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app
from pkg.forms import Farmerlogform, Farmersignform, FarmerAddProductForm
from pkg.models import Farmer, Restaurant, db, Product, Category


@app.route('/signup/', methods=['GET', 'POST'])
def general_signup():
    return render_template("signup.html")


@app.route('/login/')
def login():
    rest_deets = 'None'
    return render_template('login.html', rest_deets=rest_deets)


@app.route('/farmer-signup/', methods=['GET', 'POST'])
def handle_farmer_signup():
    farmer = Farmersignform()
    print(request.method)
    if request.method == 'GET':
        return render_template('user_farmer/farmer_signup.html', farmer=farmer)
    else:
        if farmer.validate_on_submit():
            farm_name = request.form.get('farm_name')
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            phone_number = request.form.get('phone_number')
            state = request.form.get('state')
            print(state)
            address = request.form.get('address')
            email = request.form.get('email')
            username = request.form.get('username')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            if password != confirm_password:
                flash('errormsg', 'Password mismatch please try again')
                return redirect('/farmer-signup/')
            else:
                hashed = generate_password_hash(password)
                push_to_db = Farmer(farm_name=farm_name,
                                    farmer_first_name=firstname,
                                    farmer_last_name=lastname,
                                    farmer_phone_number=phone_number,
                                    farmer_email=email,
                                    farmer_state_id=state,
                                    farmer_address=address,
                                    farmer_username=username,
                                    farmer_password=hashed)
                db.session.add(push_to_db)
                db.session.commit()
                flash("feedback", 'An account has been created for you')
                return redirect('/farmer-login/')
    return render_template('user_farmer/farmer_signup.html', farmer=farmer)


@app.route('/farmer-login/', methods=['GET', 'POST'])
def farmer_login():
    farmer = Farmerlogform()
    if request.method == "GET":
        return render_template('user_farmer/farmer_login.html', farmer=farmer)
    else:
        if farmer.validate_on_submit():
            email = request.form.get('email')
            password = request.form.get('password')
            print(password)
            check_record = db.session.query(Farmer).filter(Farmer.farmer_email == email).first()
            print(check_record)
            if check_record:
                hashed_password = check_record.farmer_password
                print(hashed_password)
                chk = check_password_hash(hashed_password, password)
                print(chk)
                if chk:
                    session["farmer_loggedin"] = check_record.farm_id
                    return redirect('/farmer-dashboard/')
                else:
                    flash('errors', 'Invalid Password')
                    return redirect('/farmer-login/')
            else:
                flash('errors', 'Invalid Email')
                return redirect('/farmer-login/')

    return render_template('user_farmer/farmer_login.html', farmer=farmer)


@app.route('/farmer-dashboard/')
def farmer_dashboard():
    farmer_id = session.get("farmer_loggedin")
    if not farmer_id:
        flash('errors', 'You need to log in first!')
        return redirect('/farmer-login/')

    farmer = db.session.query(Farmer).filter(Farmer.farm_id == farmer_id).first()

    if not farmer:
        flash('errors', 'Cannot find farmer with this id!')
        return redirect('/farmer-login/')

    farmer_name = f"{farmer.farmer_first_name}"
    # Query to fetch products and join with category to get the category name
    products = db.session.query(
        Product,
        Category.category_name
    ).join(
        Category, Category.category_id == Product.pro_category_id
    ).filter(
        Product.farm_id == farmer_id
    ).all()
    return render_template(
        'user_farmer/farmer_view_products.html',
        farmer_name=farmer_name,
        products=products
    )


@app.route("/farmer-logout/")
def farmer_logout():
    session.pop('farmer_loggedin', None)
    return redirect('/')


@app.route('/farmer-add-product/', methods=["GET", "POST"])
def farmer_add_product():
    farmer_id = session.get("farmer_loggedin")
    if not farmer_id or not db.session.query(
            Farmer).filter(Farmer.farm_id == farmer_id).first():
        flash('errors', 'You need to log in first!')
        return redirect('/farmer-login/')
    form = FarmerAddProductForm()
    form.populate_categories()
    if request.method == "GET" or not form.validate_on_submit():
        return render_template(
            'user_farmer/farmer_add_products.html',
            form=form)

    # Handle form submission
    new_product = Product(
        pro_name=form.pro_name.data,
        pro_category_id=form.pro_category_id.data,
        qua_avail=form.qua_avail.data,
        price_per_unit=form.price_per_unit.data,
        pro_status=form.pro_status.data,
        farm_id=farmer_id
        # Get the farmer ID from session
    )
    # Handle file upload
    if form.pro_picture.data:
        new_product.pro_picture = form.pro_picture.data.read(
        )  # Storing the file as binary

    db.session.add(new_product)
    db.session.commit()
    flash('Product added successfully!', 'success')
    return redirect(url_for('farmer_dashboard'))