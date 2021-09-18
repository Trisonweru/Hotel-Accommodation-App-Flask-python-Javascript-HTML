from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
import os


basedir=os.path.abspath(os.path.dirname(__file__)) #gets the base direcotry to our app.

app = Flask(__name__) #creates a flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' #configure myshop database
app.config['SQLALCHEMY_BINDS'] = {
    'data':'sqlite:///dataDB.db',
    'bookings':'sqlite:///bookingsDB.db',
    }#use other separate databases for different tasks in the app.

app.config['STRIPE_PUBLIC_KEY']='pk_test_51Hb7T9LEdnNAm34FNAN277FHhXQb0kXtTD8sKUmKyfe9DM5QvDAhxRYRXOCffV1705ou7YveDaZtCK3Mt8QJQ24I00qmOyFPuE'
app.config['STRIPE_SECRET_KEY']='sk_test_51Hb7T9LEdnNAm34FM39TocpnPkcAMBt3NrFBIWpnDqsNSpQyu1sXONXIo5AboR0zPUUKrzgAo8xtZ4cvYM2H1WLm007wTlsrpO'
app.config['SECRET_KEY']='thisissupposedtobemysecret' #configure a secret key

app.config['UPLOADED_PHOTOS_DEST']=os.path.join(basedir, "static/images") #configures the destitanation for uploaded image files
#requrement configugurations for whenever you would like to upload images 
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app) 
SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy(app)# creates a database
bcrypt=Bcrypt(app)# instatiate the bcrypt to help in hashing of passwords

from Application.home import routes
from Application.auth import routes
from Application.dashboard import routes
