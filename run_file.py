from pkg import create_app, db

app = create_app()

with app.app_context():
    db.create_all()
    from pkg import restaurant_routes, farmer_routes, admin_routes
    from pkg import forms
    from setup import *
    create_states()
    create_categories()
    create_farmer_and_products()

if __name__ == "__main__":
    app.run(debug=True)
