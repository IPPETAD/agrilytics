from farm import app
from flask import render_template, request

from flask.ext.pymongo import PyMongo
from bson.objectid import ObjectId

mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('home.html')
    
@app.route('/fields')
def fields():
    fields = mongo.db.fields.find()
    return render_template('fields.html', fields = fields)
    
@app.route('/field/<field_id>')
def field(field_id):
    field = mongo.db.fields.find_one({"_id": ObjectId(field_id) })
    return render_template('field.html', field = field)
    
@app.route('/market')
def marketplace():
    crop = request.args.get("crop")
    listings = mongo.db.offers.find({"crop": crop})
    return render_template('marketplace.html', offers = listings)