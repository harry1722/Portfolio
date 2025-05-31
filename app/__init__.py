from flask import Flask

app = Flask(__name__)
app.secret_key = 'tanismevjennemendjenjesecretkeyndajposhkruajkete'  # vendos ndonjë string të fortë këtu


from app import routes
