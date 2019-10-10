import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

host = os.environ.get('MONGODB_URI')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
# REMOVE
# db.shoes.drop()

shoes = db.shoes

app = Flask(__name__)

@app.route('/')
def shoes_index():
    """Show all shoes"""
    return render_template('shoes_index.html.j2', shoes=shoes.find())

@app.route('/shoes/new')
def shoes_new():
    """Create a new shoe"""
    return render_template('shoes_new.html.j2', shoe={}, title='Add Shoe')

@app.route('/shoes', methods=['POST'])
def shoes_submit():
    """Submit new shoe"""
    shoe = {
        'name': request.form.get('name'),
        'price': request.form.get('price'),
        'image_url': request.form.get('image_url'),
        'description': request.form.get('description')
    }
    print(shoe)
    shoe_id = shoes.insert_one(shoe).inserted_id
    return redirect(url_for('shoes_show', shoe_id=shoe_id))

@app.route('/shoes/<shoe_id>')
def shoes_show(shoe_id):
    """Show an individual shoe"""
    shoe = shoes.find_one({'_id': ObjectId(shoe_id)})
    return render_template('shoes_show.html.j2', shoe=shoe)

@app.route('/shoes/<shoe_id>/edit')
def shoes_edit(shoe_id):
    """Display the edit form"""
    shoe = shoes.find_one({'_id': ObjectId(shoe_id)})
    return render_template('shoes_edit.html.j2', shoe=shoe, title='Update Shoe')

@app.route('/shoes/<shoe_id>', methods=['POST'])
def shoes_update(shoe_id):
    """Update shoe"""
    updated_shoe = {
        'name': request.form.get('name'),
        'price': request.form.get('price'),
        'image_url': request.form.get('image_url'),
        'description': request.form.get('description')
    }
    shoes.update_one(
        {'_id': ObjectId(shoe_id)},
        {'$set': updated_shoe}
    )
    return redirect(url_for('shoes_show', shoe_id=shoe_id))

@app.route('/shoes/<shoe_id>/delete', methods=['POST'])
def shoes_delete(shoe_id):
    """Remove a shoe"""
    shoes.delete_one({'_id': ObjectId(shoe_id)})
    return redirect(url_for('shoes_index'))