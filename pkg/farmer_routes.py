from flask import render_template, redirect, flash, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from pkg import app
from pkg.forms import Farmerlogform, Farmersignform
from pkg.models import Farmer, Restaurant, db


@app.route('/login/')
def login():
    return render_template('login.html')


@app.route('/signup/', methods=['GET','POST'])
def general_signup():
    return render_template("signup.html")

# Route for the farmer dashboard
@app.route('/farmer-dashboard/')
def farmer_dashboard():
    return render_template('user/farmer-dashboard.html')

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
    


# @app.route('/register/',methods=['POST','GET'])
# def user_register():
#     if request.method == 'GET':
#         return render_template('user/register.html')
#     else:
#         #retrieve forms value and validate
#         email = request.form.get('bizemail')#request.form['email']
#         password = request.form.get('bizpass')
#         cpassword = request.form.get('bizconfirm')
#         name = request.form.get('bizname')
#         if password != cpassword:
#             flash('errormsg', 'Password mismatch please try again')
#             return redirect('/register/')
#         else:
#             hashed = generate_password_hash(password)
#             b = Business(biz_name=name,biz_password=hashed,biz_email=email)
#             db.session.add(b)
#             db.session.commit()
#             flash("feedback", 'An account has been created for you')

#             return redirect('/login/')

@app.route('/farmer-login/', methods=['GET', 'POST'])
def handle_farmer_login():
    farmer = Farmerlogform()
    if farmer.validate_on_submit():
        email = farmer.email.data
        password = farmer.password.data  
        return redirect(url_for('farmer_dashboard'))
    print(farmer)
    return render_template('user_farmer/farmer_login.html', farmer=farmer)