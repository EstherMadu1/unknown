import os
from flask import Flask 
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from dotenv import load_dotenv
from pkg.models import db
load_dotenv()


csrf = CSRFProtect()


def create_app():
    from pkg import models
    app = Flask(__name__,instance_relative_config=True,template_folder='pages')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config.from_pyfile("config.py")
    db.init_app(app)
    migrate = Migrate(app,db)
    
    return app

app = create_app()



from pkg import restaurant_routes, farmer_routes
from pkg import forms