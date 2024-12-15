from pkg import create_app, db

app = create_app()


with app.app_context():
    db.create_all()
    from pkg import restaurant_routes, farmer_routes, admin_routes
    from pkg import forms

if __name__ == "__main__":
    app.run(debug=True)
