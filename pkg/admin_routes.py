from flask import render_template, redirect, flash, session, request, url_for
from werkzeug.security import check_password_hash
from flask import current_app as app
from pkg.models import db, Farmer, Restaurant, Admin
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
                flash("Login Successful!", "success")
                return redirect(url_for('admin_show_farmer'))
            else:
                flash("danger", "Invalid Password" )
        else:
            flash( "danger", "Invalid Username", )

        return redirect(url_for('admin_login'))

    return render_template('admin/admin_login.html', admin=admin)



@app.route('/admin-dashboard/')
def admin_show_farmer():
    admin_id = session.get("admin_loggedin")
    if admin_id:
        admin = db.session.query(Admin).all()
    else:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for('admin_login'))

    farmers_deets = db.session.query(Farmer).all()
    rest_deets = db.session.query(Restaurant).all()
    admin_deets = db.session.query(Admin).all()
    print(admin_deets)
    return render_template('admin/admin.html',farmers_deets=farmers_deets,rest_deets=rest_deets, admin_deets=admin_deets)


@app.route('/delete-farmer/<int:farm_id>', methods=['POST'])
def delete_farmer(farm_id):
    farmer = Farmer.query.get_or_404(farm_id)  # Use correct argument name
    db.session.delete(farmer)  # Delete farmer from the database
    db.session.commit()  # Commit changes
    flash(f"Farmer with ID {farm_id} has been deleted successfully.", "success")
    return redirect(url_for('admin_show_farmer'))
