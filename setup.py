from datetime import datetime
import os
import shutil


def create_states():
    from pkg.models import State, db
    # List of all states in Nigeria
    nigeria_states = [
        "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue",
        "Borno", "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu",
        "Gombe", "Imo", "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi",
        "Kogi", "Kwara", "Lagos", "Nasarawa", "Niger", "Ogun", "Ondo",
        "Osun", "Oyo", "Plateau", "Rivers", "Sokoto", "Taraba", "Yobe", "Zamfara",
        "FCT"
    ]

    # Check if the states already exist in the database
    existing_states = State.query.count()
    if existing_states > 0:
        print(f"{existing_states} states already exist in the database. No new states added.")
        return

    # Insert states into the table
    for state in nigeria_states:
        new_state = State(state_name=state)
        db.session.add(new_state)

    # Commit changes to the database
    db.session.commit()
    print(f"Added {len(nigeria_states)} states to the database.")


def create_categories():
    from pkg.models import Category, db
    # List of categories to populate
    categories = ["Proteins", "Barn Products", "Legumes", "Vegetables"]

    # Check if the categories already exist in the database
    existing_categories = Category.query.count()
    if existing_categories > 0:
        print(f"{existing_categories} categories already exist in the database. No new categories added.")
        return

    # Insert categories into the table
    for category_name in categories:
        new_category = Category(category_name=category_name)
        db.session.add(new_category)

    # Commit changes to the database
    db.session.commit()
    print(f"Added {len(categories)} categories to the database.")


def create_farmer_and_products():
    from pkg.models import Farmer, Product, db, Category

    source_folder = os.path.join("pkg", "static/assets/images")  # Folder containing carrot.jpg, etc.
    destination_folder = os.path.join("pkg", "static/uploaded")

    # Check if the farmer already exists
    farmer_username = "unique_far"
    existing_farmer = Farmer.query.count()

    if existing_farmer:
        print("Farmer already exists in the database.")
        return

    # Create the farmer
    new_farmer = Farmer(
        farm_name="Green Acres",
        farmer_first_name="John",
        farmer_last_name="Doe",
        farmer_phone_number="08012345678",
        farmer_email="johndoe@example.com",
        farmer_state_id=1,  # Replace with a valid state_id from the `states` table
        farmer_address="123 Green Acres Street, Farmland City",
        farmer_username=farmer_username,
        farmer_password="hashed_password_here",  # Use a password hashing mechanism like bcrypt
        date_registered=datetime.utcnow(),
    )
    db.session.add(new_farmer)
    db.session.flush()  # Flush to get the `farm_id` for the new farmer

    # Predefined product data
    products_data = [
        {"pro_name": "Carrot", "pro_category": "Vegetables", "qua_avail": 100, "price_per_unit": 50.00,
         "pro_picture": "carrot.jpg"},
        {"pro_name": "Broccoli", "pro_category": "Vegetables", "qua_avail": 80, "price_per_unit": 70.00,
         "pro_picture": "brocoli.jpg"},
        {"pro_name": "Cabbage", "pro_category": "Vegetables", "qua_avail": 120, "price_per_unit": 40.00,
         "pro_picture": "cabbage.jpg"},
        {"pro_name": "Chicken", "pro_category": "Proteins", "qua_avail": 50, "price_per_unit": 500.00,
         "pro_picture": "chicken.jpg"},
        {"pro_name": "Tomato", "pro_category": "Vegetables", "qua_avail": 200, "price_per_unit": 30.00,
         "pro_picture": "tomato.jpg"},
        {"pro_name": "Orange", "pro_category": "Barn Products", "qua_avail": 150, "price_per_unit": 60.00,
         "pro_picture": "orange.jpg"},
        {"pro_name": "Egg", "pro_category": "Proteins", "qua_avail": 300, "price_per_unit": 20.00,
         "pro_picture": "egg.jpg"},
    ]

    # Add products for the farmer
    for product in products_data:
        # Find the category for the product
        category = Category.query.filter_by(category_name=product["pro_category"]).first()
        if not category:
            print(f"Category {product['pro_category']} does not exist. Skipping product {product['pro_name']}.")
            continue
        # Copy the image to the destination folder
        source_file = os.path.join(source_folder, product["pro_picture"])
        destination_file = os.path.join(destination_folder, product["pro_picture"])

        try:
            shutil.copy(source_file, destination_file)
            print(f"Copied {product['pro_picture']} to {destination_folder}.")
        except FileNotFoundError:
            print(
                f"Image {product['pro_picture']} not found in {source_folder}. Skipping product {product['pro_name']}.")
        new_product = Product(
            pro_name=product["pro_name"],
            pro_category_id=category.category_id,
            qua_avail=product["qua_avail"],
            price_per_unit=product["price_per_unit"],
            farm_id=new_farmer.farm_id,
            pro_picture=product["pro_picture"],
        )
        db.session.add(new_product)

    # Commit changes to the database
    db.session.commit()
    print("Farmer and products created successfully.")
