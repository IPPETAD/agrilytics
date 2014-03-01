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
	
@app.route('/bins')
def bins():
    bins = mongo.db.bins.find()
    return render_template('bins.html', bins = bins)
    
@app.route('/field/<field_id>')
def field(field_id):
    field = mongo.db.fields.find_one({"_id": ObjectId(field_id) })
    return render_template('field.html', field = field)
    
@app.route('/bin/<bin_id>')
def bin(bin_id):
    bin = mongo.db.bins.find_one({"_id": ObjectId(bin_id) })
    return render_template('bin.html', bin = bin)
    