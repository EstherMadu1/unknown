from flask import render_template, redirect, flash, session, request, url_for
from werkzeug.security import check_password_hash
from flask import current_app as app
from pkg.models import db, Farmer, Restaurant, Admin, Category, Product
from pkg.forms import AdminLoginForm


# Route for admin login
@app.route('/admin/', methods=['GET', 'POST'])
def admin_login():
    admin = AdminLoginForm()
    if admin.validate_on_submit():  # This ensures the form is submitted and valid
        username = request.form.get('username')
        password = request.form.get('password')

        check_record = db.session.query(Admin).filter_by(admin_username=username).first()
        print(check_record)
        if check_record:
            hashed_password = check_record.admin_password
            if check_password_hash(hashed_password, password):
                session['admin_loggedin'] = check_record.admin_id
                return redirect(url_for('admin_show_farmer'))
            else:
                flash("errors", "Invalid Password" )
        else:
            flash( "errors", "Invalid Username", )

        return redirect(url_for('admin_login'))

    return render_template('admin/admin_login.html', admin=admin)



@app.route('/admin-dashboard/')
def admin_show_farmer():
    adminn_id = session.get("admin_loggedin")
    
    if not adminn_id:
        flash("errors", "Please log in to access the dashboard.")
        return redirect(url_for('admin_login'))

    admin = db.session.query(Admin).filter(Admin.admin_id == adminn_id).first()
    if not admin:
        flash("errors","Invalid session. Please log in again.", )
        return redirect(url_for('admin_login'))


    admin_name = f"{admin.admin_username}"
    farmers_deets = db.session.query(Farmer).all()
    rest_deets = db.session.query(Restaurant).all()
    category = db.session.query(Category).all()

    return render_template(
        'admin/admin.html',
        admin_name=admin_name,
        farmers_deets=farmers_deets,
        rest_deets=rest_deets,
        category=category
    )
    
@app.route("/admin-logout/")
def admin_logout():
    session.pop('admin_loggedin', None)
    return redirect('/')



# @app.route('/delete-farmer/<int:farm_id>', methods=['POST'])
# def delete_farmer(farm_id):
#     farmer = Farmer.query.get_or_404(farm_id)  # Use correct argument name
#     db.session.delete(farmer)  # Delete farmer from the database
#     db.session.commit()  # Commit changes
#     flash(f"Farmer with ID {farm_id} has been deleted successfully.", "success")
#     return redirect(url_for('admin_show_farmer'))
