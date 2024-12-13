from flask import render_template, redirect, flash, request, url_for
from pkg import app

# Route for the admin page
@app.route('/admin/')
def admin():
    return render_template('admin/admin.html')

# Route for admin login
@app.route('/admin-login/')
def admin_login():
    return render_template('admin/admin_login.html')