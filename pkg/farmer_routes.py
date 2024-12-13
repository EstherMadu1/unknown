from flask import render_template, redirect, flash, request, url_for,session
from werkzeug.security import generate_password_hash, check_password_hash
from pkg import app
from pkg.forms import Farmerlogform, Farmersignform
from pkg.models import Farmer, Restaurant, db



@app.route('/signup/', methods=['GET','POST'])
def general_signup():
    return render_template("signup.html")

@app.route('/login/')
def login():
    rest_deets='None'
    return render_template('login.html', rest_deets=rest_deets)



@app.route('/farmer-signup/', methods=['GET','POST'])
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
            address = request.form.get('address')
            email = request.form.get('email')
            username = request.form.get('username')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            if password != confirm_password:
                flash('errormsg', 'Password mismatch please try again')
                return redirect ('/farmer-signup/')
            else:
                hashed=generate_password_hash(password)
                push_to_db= Farmer(farm_name=farm_name,farmer_first_name=firstname, farmer_last_name=lastname, farmer_phone_number=phone_number, farmer_email=email,farmer_state_id=state,farmer_address=address,farmer_username=username,farmer_password=hashed)
                db.session.add(push_to_db)
                db.session.commit()
                flash("feedback", 'An account has been created for you')
                return redirect('/farmer-login/')
    return render_template('user_farmer/farmer_signup.html', farmer=farmer)  


@app.route('/farmer-login/', methods=['GET', 'POST'])
def farmer_login(): 
    farmer = Farmerlogform()
    if request.method == "GET":
        return render_template('user_farmer/farmer_login.html',farmer=farmer) 
    else:
        if farmer.validate_on_submit():
            email=request.form.get('email')
            password=request.form.get('password')
            print(password)
            check_record=db.session.query(Farmer).filter(Farmer.farmer_email==email).first()
            print(check_record) 
            if check_record:
                hashed_password = check_record.farmer_password
                print(hashed_password)
                chk= check_password_hash(hashed_password,password)
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
        else:
            for field, errors in farmer.errors.items():
                for error in errors:
                    flash(f"Error in {field}: {error}", 'error')
    
    return render_template('user_farmer/farmer_login.html',farmer=farmer)


@app.route('/farmer-dashboard/')
def farmer_dashboard():
    farmer_id = session.get("farmer_loggedin")
    if farmer_id:
        farmer = db.session.query(Farmer).filter(Farmer.farm_id == farmer_id).first()
        if farmer:
            farmer_name = f"{farmer.farmer_first_name}"
            return render_template('user_farmer/farmer_dashboard.html', farmer_name=farmer_name)
        flash('errors', 'You need to log in first!')
        return redirect('/farmer-login/')
    return render_template('user_farmer/farmer_dashboard.html')


@app.route("/farmer-logout/")
def farmer_logout():
    session.pop('farmer_loggedin', None)
    return redirect('/')
