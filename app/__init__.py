from flask import Flask
import os

app = Flask(__name__)
app.secret_key = 'tanismevjennemendjenjesecretkeyndajposhkruajkete'  

# Add this config here, right after app is created:
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

# Make sure uploads folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

from app import routes
