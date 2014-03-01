from farm import app
from farm import forms
from flask import render_template, request
from flask_wtf.csrf import CsrfProtect

from flask.ext.pymongo import PyMongo
from bson.objectid import ObjectId

mongo = PyMongo(app)
csrf = CsrfProtect(app)

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
    
@app.route('/field/add', methods=['GET', 'POST'])
def field_add():
    if request.method == 'POST':
        return render_template('field_add.html', form=form)
    else:
        form = forms.FieldForm()
        return render_template('field_add.html', form=form)










# For debugging, not production
app.secret_key = '\xe2t\xebJ\xb7\xf0r\xef\xe7\xe6\\\xf5_G\x0b\xd5B\x94\x815\xc1\xec\xda,'
