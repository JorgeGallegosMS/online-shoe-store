import os
from flask import Flask, render_template
from pymongo import MongoClient

host = os.environ.get('MONGODB_URI')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
db.shoes.drop()

shoes = db.shoes

app = Flask(__name__)

@app.route('/')
"""Show all shoes"""
def shoes_index():
    return render_template('shoes_index.html.j2', shoes=shoes.find())