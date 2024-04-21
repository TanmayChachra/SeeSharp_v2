from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import os
import shutil

db = SQLAlchemy()
DB_NAME = "database.db"
UPLOAD_FOLDER = "website\\static\\test_images"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'saudfbajskbrakdnsafjln12321n4ln'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    db.init_app(app) # initialize the database and bind with the app 

    from .views import views
    from .auth import auth 

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    from .models import Staff,Students,Classes,Admin

    # create database
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # where should user go if he is not logged in 
    login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_staff_user(staff_id):
    #     return Staff.query.get(int(staff_id))
    
    # @login_manager.user_loader
    # def load_admin_user(admin_id):
    #     return Admin.query.get(int(admin_id))
    
    @login_manager.user_loader
    def load_user(user_id):
        # Check if the user's email starts with 'admin_'
        admin_user = Admin.query.filter_by(admin_id=user_id).filter(Admin.email.startswith('admin')).first()
        if admin_user:
            return admin_user
        else:
            # Check if the user's email starts with 'user_'
            staff_user = Staff.query.filter_by(staff_id=user_id).filter(Staff.email.startswith('s')).first()
            return staff_user
    return app

def remove_contents(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)