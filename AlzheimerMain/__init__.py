from PIL import Image 
from fastai.vision import *
from fastai.metrics import accuracy
import pickle
import os
import sqlite3
from flask_sqlalchemy import SQLAlchemy

from skimage import io
from flask import Flask
import joblib
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)

app.config["SECRET_KEY"]='DQ4YlKxRuJ6gOPhry8chBw'
app.config["ALLOWED_IMAGE_EXTENSIONS"]=["PNG","JPG","JPEG"]
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///arp.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
from AlzheimerMain import routes