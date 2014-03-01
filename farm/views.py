from farm import app
from farm import forms
from flask import render_template, request
from flask_wtf.csrf import CsrfProtect

from flask.ext.pymongo import PyMongo
from bson.objectid import ObjectId

app.config['MONGO_URI'] = 'mongodb://farmspot:farmspot@troup.mongohq.com:10058/FarmSpot'

mongo = PyMongo(app)
csrf = CsrfProtect(app)

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

@app.route('/market')
def marketplace():
    crop = request.args.get("crop")
    offers = mongo.db.offers.find({"crop": crop})
    crop_types = mongo.db.crop_types.find()
    return render_template('marketplace.html', offers = offers, crop = crop, crop_types = crop_types)

@app.route('/field/add', methods=['GET', 'POST'])
def field_add():
    form = forms.FieldForm()
    if request.method == 'POST':
        return render_template('field_add.html', form=form)
    else:
        return render_template('field_add.html', form=form)

@app.route('/bin/<bin_id>')
def bin(bin_id):
    bin = mongo.db.bins.find_one({"_id": ObjectId(bin_id) })
    return render_template('bin.html', bin = bin)

# For debugging, not production
app.secret_key = '\xe2t\xebJ\xb7\xf0r\xef\xe7\xe6\\\xf5_G\x0b\xd5B\x94\x815\xc1\xec\xda,'
