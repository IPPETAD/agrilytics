from farm import app
from farm import forms
from flask import render_template, request, url_for, redirect
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

@app.route('/bins')
def bins():
    bins = mongo.db.bins.find()
    return render_template('bins.html', bins = bins)

@app.route('/field/<field_id>/')
def field(field_id):
    field = mongo.db.fields.find_one({"_id": ObjectId(field_id) })
    return render_template('field.html', field = field)

@app.route('/field/add', methods=['GET', 'POST'])
def field_add():
    form = forms.FieldForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            post = {"name": form.name.data, "size": form.size.data, "geo": form.geo_data.data, "section": []}
            field_id = mongo.db.fields.insert(post)
            return redirect(url_for('.field', field_id=field_id))
    else:
        return render_template('field_add.html', form=form)

@app.route('/field/<field_id>/section/add', methods=['GET','POST'])
def section_add(field_id):
    form = forms.SectionForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            field = mongo.db.fields.find_one({'_id': ObjectId(field_id)})
            if 'section' not in field.keys():
                field['section'] = []
            field['section'].append({'name': form.name.data, 'crop': form.crop.data, 'acres': form.acres.data})
            field_id = mongo.db.fields.save(field)
            return redirect(url_for('field', field_id=field_id))
    else:
        return render_template('section_add.html', form=form, field_id=field_id)
        

@app.route('/bin/<bin_id>')
def bin(bin_id):
    bin = mongo.db.bins.find_one({"_id": ObjectId(bin_id) })
    return render_template('bin.html', bin = bin)

# For debugging, not production
app.secret_key = '\xe2t\xebJ\xb7\xf0r\xef\xe7\xe6\\\xf5_G\x0b\xd5B\x94\x815\xc1\xec\xda,'
